uvicorn main:create_app --factory --app-dir=./ --reload --host=0.0.0.0 --port=8080  --no-use-colors --loop=uvloop --timeout-keep-alive 10
