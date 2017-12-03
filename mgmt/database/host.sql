-- -----------------------------------------------------
-- Add sample data to host relation
-- Author: Hoanh An (hoanhan@bennington.edu)
-- Date: 12/2/17
-- -----------------------------------------------------

INSERT INTO "host" VALUES (DEFAULT, '10.10.127.100:5000','Crawler', 'online', 'healthy');
INSERT INTO "host" VALUES (DEFAULT, '10.10.127.101:5000','Crawler', 'waiting', 'failure');
INSERT INTO "host" VALUES (DEFAULT, '10.10.127.102:5000','Index Builder', 'online', 'healthy');
INSERT INTO "host" VALUES (DEFAULT, '10.10.127.103:5000','Index Builder', 'waiting', 'healthy');
INSERT INTO "host" VALUES (DEFAULT, '10.10.127.104:5000','Index Server', 'waiting', 'failure');
INSERT INTO "host" VALUES (DEFAULT, '10.10.127.105:5000','Index Server', 'online', 'healthy');
