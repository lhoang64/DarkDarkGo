-- -----------------------------------------------------
-- Add sample data to crawler relation
-- Author: Hoanh An (hoanhan@bennington.edu)
-- Date: 12/2/17
-- -----------------------------------------------------

INSERT INTO "crawler" VALUES (DEFAULT, 1, '10.10.127.100:5000', 'propagated');
INSERT INTO "crawler" VALUES (DEFAULT, 2, '10.10.127.100:5000', 'crawled');
INSERT INTO "crawler" VALUES (DEFAULT, 3, '10.10.127.100:5000', 'crawled');
INSERT INTO "crawler" VALUES (DEFAULT, 4, '10.10.127.101:5000', 'crawling');
INSERT INTO "crawler" VALUES (DEFAULT, 5, '10.10.127.101:5000', 'crawling');