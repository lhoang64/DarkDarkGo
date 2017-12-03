## Index Builder

The folder contains several files. Description of each file can be found below:

#### index\_builder\_final.py: 

- Status: Completed
- Description: a class for Index_Builder, in charge of building the index chunk for each content chunk.
- Input: chunk_id + directory/file name of content chunk
- Output: json file containing the index chunk

#### index\_builder\_server.py:

- Status: Ongoing
- Description: List of endpoints to interact with Index Server
	- URL: `/indexed_chunk/<string:chunk_id>`
	- Method: `GET`
	- Return index chunk given chunk_id
	- Sample data:
		```
		[
		{
			"word": "nuclear", 
			"word_count": 7, 
			"doc_ID": ["32-abc3"]
		}, ...
		]
		```
		
#### testing.py:

I will have three endpoints interaction with Mgmt, including `/set_component_state`, `/get_content_chunk_metadata`, and `/set_index_chunk_metadata` (details of these APIs can be found in Mgmt API doc. In addition, I also have one endpoint interaction with Crawler, which is `/get_chunk/<string:chunk_id>`.

I, therefore, wrote two files mgmt\_server.py and crawler\_server.py, which can be used to test the dummy data. In order to run this test, put mgmt\_server.py and chunk\_metadata.json in the same directory, and run it on one server. Put crawler\_server and four content chunk files in the same directory and run it on another server. **Note: You will need to change mgmt\_ip\_addr and crawler\_ip\_addr in testing.py before compiling.**

#### Sample_files

This folder contains all the content chunk files and index chunk files in json format.

