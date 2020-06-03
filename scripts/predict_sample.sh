curl --location --request POST 'http://localhost:8080/microservice/RandomForestMicroservice/endpoint_predict' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "command": "predict",
  "data": [[1, 2, 3], [1, 3, 4]]
}'