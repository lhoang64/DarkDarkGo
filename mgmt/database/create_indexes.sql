-- -----------------------------------------------------
-- Create indexes for faster retrieval
-- Author: Hoanh An (hoanhan@bennington.edu)
-- Date: 12/4/17
-- -----------------------------------------------------

CREATE UNIQUE INDEX link_chunk_id_idx on link (chunk_id);
CREATE UNIQUE INDEX chunk_id_idx on chunk (id);
CREATE UNIQUE INDEX host_idx on host (host);
CREATE UNIQUE INDEX crawler_chunk_id_idx on crawler (chunk_id);
CREATE UNIQUE INDEX crawler_c_host_idx on crawler (c_host);
CREATE UNIQUE INDEX index_builder_chunk_id_idx on index_builder (chunk_id);
CREATE UNIQUE INDEX index_builder_ib_host_idx on index_builder (ib_host);
CREATE UNIQUE INDEX index_server_row_idx on index_server (row);
CREATE UNIQUE INDEX index_server_chunk_id_idx on index_server (chunk_id);
CREATE UNIQUE INDEX index_server_is_host_idx on index_server (is_host);