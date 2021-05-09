#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

es_url="http://localhost:9200"
index_list='aips aipfiles transfers transferfiles'

if ! command -v jq &> /dev/null
then
  echo "Please, install jq package before running the script ('apt-get install jq' or 'yum install jq')"
  exit 1
fi

echo -e "\nIndex list before reindexing:\n"
curl -s -X GET "${es_url}/_cat/indices/%2A?v=&s=index:desc"
echo -e "\n"

echo "Please back up your Elasticsearch indices before proceeding further."
read -r -p "Do you want to continue? [y/N] " response
case "$response" in
    [yY])
        ;;
    *)
        exit 1
        ;;
esac

# Delete new indices
for index in $index_list; do
  echo -e "Deleting ${index}_new..."
  curl -s -X DELETE ${es_url}/${index}_new > /dev/null
done

# Create tmp indices with old mappings
for index in $index_list; do
  echo -e "Creating ${index}_new with old mappings..."
  curl -s -XPUT ${es_url}/${index}_new \
    -H 'Content-Type: application/json' \
    -d "$(curl -s ${es_url}/${index} | jq '.'"${index}"' | del(.settings.index.provided_name, .settings.index.creation_date, .settings.index.uuid, .settings.index.version)')"  > /dev/null
done
echo -e "\n"

# Clone indices with _reindex API call:
for index in $index_list; do
    echo "Reindex ${index} in ${index}_new..."
    curl -s -X POST \
      ${es_url}/_reindex \
      -H 'Content-Type: application/json' \
      -d '{
      "conflicts": "proceed",
      "source": {
        "index": "'"${index}"'"
      },
      "dest": {
        "index": "'"${index}_new"'",
        "version_type": "external"
      }
    }'  > /dev/null
done
echo -e "\n\n"

echo -e "Index list after tmp indices creation\n"
sleep 30 # Wait 30s to update elasticsearch list
indices_output=$(curl -s -X GET "${es_url}/_cat/indices/%2A?v=&s=index:desc")
curl -s -X GET "${es_url}/_cat/indices/%2A?v=&s=index:desc"
echo -e "\n"

# Delete old indices
for index in $index_list; do
  echo "Deleting ${index}..."
  curl -s -X DELETE ${es_url}/${index} > /dev/null
done

# Restart archivematica-dashboard to create indices with new mappings
echo -e "\nRestarting archivematica-dashboard"
sudo service archivematica-dashboard restart
# docker-compose restart archivematica-dashboard

# Wait 30 seconds
echo "Wait 30 seconds to ensure dashboard has created the empty indices with new mapping"
sleep 30
echo -e "\n"

# When index has no docs the reindex doesn't create the new index (typically transferfiles index)
# There's a check to ensure the new index has been create before reindexing.
# Reindex from *_new indices:
for index in $index_list; do
  if echo "$indices_output" | grep ${index}_new >/dev/null; then
    echo "Indexing ${index} using ${index}_new ..."
    curl -s -X POST \
      ${es_url}/_reindex \
      -H 'Content-Type: application/json' \
      -d '{
      "source": {
        "index": "'"${index}_new"'"
      },
      "dest": {
        "index": "'"${index}"'"
      }
    }' > /dev/null
  fi
done
echo -e "\n"

# Delete temporary indices
for index in $index_list; do
  if echo "$indices_output" | grep ${index}_new >/dev/null; then
     echo "Deleting ${index}_new..."
     curl -s -X DELETE ${es_url}/${index}_new > /dev/null
  fi
done
echo -e "\n\n"

echo "Reindexing done. The list of indices will be displayed again momentarily."
sleep 30 # Wait 30s to update elasticsearch list
curl -s -X GET "${es_url}/_cat/indices/%2A?v=&s=index:desc"

echo -e "\n"
