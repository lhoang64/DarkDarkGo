-- -----------------------------------------------------
-- mgmt_db's schema
-- Author: Hoanh An (hoanhan@bennington.edu)
-- Date: 12/2/17
-- -----------------------------------------------------


-- -----------------------------------------------------
-- Table mgmt_db.chunk
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS chunk (
  index SERIAL NOT NULL,
  id INT UNIQUE NOT NULL,
  state VARCHAR(22) NULL,
  PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table mgmt_db.link
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS link (
  index SERIAL NOT NULL,
  link VARCHAR(22) UNIQUE NOT NULL,
  chunk_id INT NOT NULL,
  state VARCHAR(22) NULL,
  PRIMARY KEY (link));


-- -----------------------------------------------------
-- Table mgmt_db.host
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS host (
  index SERIAL NOT NULL,
  host VARCHAR(22) NOT NULL,
  type VARCHAR(22) NOT NULL,
  state VARCHAR(22) NULL,
  health VARCHAR(22) NULL,
  PRIMARY KEY (host));


-- -----------------------------------------------------
-- Table mgmt_db.crawler
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS crawler (
  index SERIAL NOT NULL,
  chunk_id INT UNIQUE NOT NULL,
  C_host VARCHAR(22) NOT NULL,
  C_task VARCHAR(22) NULL);


-- -----------------------------------------------------
-- Table mgmt_db.index_builder
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS index_builder (
  index SERIAL NOT NULL,
  chunk_id INT UNIQUE NOT NULL,
  IB_host VARCHAR(22) NOT NULL,
  IB_task VARCHAR(22) NULL);


-- -----------------------------------------------------
-- Table mgmt_db.index_server
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS index_server (
  index SERIAL NOT NULL,
  row INT NOT NULL,
  chunk_id INT NOT NULL,
  IS_host VARCHAR(22) NOT NULL);



