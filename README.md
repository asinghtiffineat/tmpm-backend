# Shopify Integration FastAPI Backend

This repository contains the FastAPI backend for a Shopify integration system. It includes API endpoints for managing product and order information synced with various Shopify stores, and is designed to work in conjunction with a React frontend and a MySQL database.

## Features

- FastAPI backend with RESTful API endpoints.
- Integration with Shopify API for product and order synchronization.
- MySQL database integration using SQLAlchemy ORM.
- Unit tests for API endpoints with mocked data.

## Requirements

- Python 3.8 or later
- MySQL Server
- Docker (optional)

## Setup

### Environment Setup

1. **Clone the Repository**
```
git clone git@github.com:asinghtiffineat/tmpm-backend.git
cd tmpm-backend
```

2. **Install Dependencies**
```
pip install -r requirements.txt
```


### Database Setup

1. **MySQL Database**
- Create a new MySQL database for the project.

2. **Environment Variables**
- Set up the following environment variables or add them to a `.env` file:
  ```
  DATABASE_URL=mysql+pymysql://username:password@host/dbname
  SHOPIFY_API_KEY=your-shopify-api-key
  SHOPIFY_API_SECRET=your-shopify-api-secret
  ```

### Running the Application

1. **Start the FastAPI Server**
```
uvicorn app.main:app --reload
```

## Running Tests

- To run the unit tests, use the following command:
```
pytest
```


## API Documentation

- Once the server is running, API documentation is available at: `http://localhost:8000/docs`

## Docker Setup (Optional)

1. **Building the Docker Image**

```
docker build -t shopify-integration-backend .
```

2. **Running the Docker Container**
You can run the container locally to test:
```
docker run -d --name shopify-backend -p 8000:8000 shopify-integration-backend
```
## Deployment

### AWS RDS - MySQL Database Setup

1. **Create an AWS RDS MySQL Instance**
   - Navigate to the RDS section in your AWS Console.
   - Click on "Create database" and select MySQL as the database engine.
   - Follow the prompts to configure your database instance (e.g., DB instance size, storage, VPC, security groups).
   - Once the database is created, note the endpoint and credentials for later use.

2. **Update Environment Variables**
   - Modify your environment variables for the database connection:
     ```
     DATABASE_URL=mysql+pymysql://username:password@rds-endpoint/dbname
     ```

### AWS Elastic Beanstalk - Backend Deployment

1. **Install the Elastic Beanstalk CLI**
```
pip install awsebcli
```

2. **Initialize Elastic Beanstalk Application**
- Navigate to your project directory in the terminal.
- Run `eb init -p python-3.8 [your-app-name] --region [your-region]`.
- Configure the AWS credentials as prompted.

3. **Create an Elastic Beanstalk Environment**
- Run `eb create [your-env-name]`.
- This will create an environment and deploy your application.

4. **Set Environment Variables in Elastic Beanstalk**
- Navigate to the Elastic Beanstalk dashboard, select your application, and go to the 'Configuration' tab.
- In the 'Software' section, add your environment variables (like `DATABASE_URL`, `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`).

5. **Deploy Application**
- After any changes, deploy your application using:
  ```
  eb deploy
  ```

### Updating the Application

- To update your application, commit your changes and use the `eb deploy` command to deploy the latest version.

### Monitoring and Logs

- AWS Elastic Beanstalk provides monitoring tools and logs. Access these via the AWS Console to monitor the health and performance of your application.


## Contributing

- Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and include tests for new features.

## License

- This project is licensed under the [MIT License](LICENSE).

