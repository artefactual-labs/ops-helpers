-- MCP dashboard cleanup SQL
-- IMPORTANT: this SQL removes data. BACKUP YOUR DATABASE FIRST !!!!

DELETE FROM Derivations;
DELETE FROM Events;
DELETE FROM FilesIdentifiedIDs;
DELETE FROM FilesIDs;
DELETE FROM FPCommandOutput;
DELETE FROM main_fpcommandoutput;

DELETE FROM Files;
DELETE FROM SIPs;
DELETE FROM Transfers;
DELETE FROM Tasks;
DELETE FROM Jobs;
