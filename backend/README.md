# Commands 

Test locally:
```bash
docker compose up --watch

Build image:
```docker build -t get_publications .```

Tag image:
```docker tag get_publications:latest [aws_account_id].dkr.ecr.us-east-1.amazonaws.com/get_publications:latest```

Push image:
```docker push [aws_account_id].dkr.ecr.us-east-1.amazonaws.com/get_publications:latest```