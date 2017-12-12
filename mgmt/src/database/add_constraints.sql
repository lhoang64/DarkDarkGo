-- -----------------------------------------------------
-- Add foreign key constraints
-- Author: Hoanh An (hoanhan@bennington.edu)
-- Date: 12/2/17
-- -----------------------------------------------------

ALTER TABLE "link" ADD CONSTRAINT fk_link_chunk_id FOREIGN KEY (chunk_id) REFERENCES chunk (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "crawler" ADD CONSTRAINT fk_crawler_chunk_id FOREIGN KEY (chunk_id) REFERENCES chunk (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "crawler" ADD CONSTRAINT fk_crawler_C_host FOREIGN KEY (C_host) REFERENCES host (host) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "index_builder" ADD CONSTRAINT fk_index_builder_chunk_id FOREIGN KEY (chunk_id) REFERENCES chunk (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "index_builder" ADD CONSTRAINT fk_index_builder_IB_host FOREIGN KEY (IB_host) REFERENCES host (host) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "index_server" ADD CONSTRAINT fk_index_server_chunk_id FOREIGN KEY (chunk_id) REFERENCES chunk (id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "index_server" ADD CONSTRAINT fk_index_server_IS_host FOREIGN KEY (IS_host) REFERENCES host (host) ON DELETE CASCADE ON UPDATE CASCADE;