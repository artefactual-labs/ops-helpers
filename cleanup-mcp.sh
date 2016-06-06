#!/bin/bash
database="MCP"

while read p; do
  echo Executing sql on MCP: $p
  #mysql --user="$user" --password="$password" --database="$database" --execute=""
  mysql --database="$database" --execute="$p"
done <cleanup-mcp.sql
