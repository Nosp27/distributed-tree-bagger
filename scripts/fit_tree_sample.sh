curl --location --request POST 'http://localhost:8080/microservice/RandomForestMicroservice/endpoint_fit' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
	"command": "fit",
	"config": {"max_depth": 3},
	"train": [[1, 2, 3], [1, 3, 4]],
	"test": [0, 1]
}'