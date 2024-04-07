<h2>Advertising service API</h2>

<h3>Tech Stack</h3>
`python 3.10`<br> `fastAPI 0.011.1`<br> `postgreSQL 15.3` <br> 
`SQLAlchemy 2.0.29`<br>`docker 7.0.0`

<h3>Features</h3>

<ul>
<li>FastAPI asynchronous backend</li>
<li>PostgreSQL as a database, SQLAlchemy as ORM, 
Alembic is responsible for migrations</li>
<li>Docker and Docker-compose integration</li>
</ul>

<h3>Config</h3>

The project is completely ready to run all the services from 
configuration file <i>docker-compose.yaml</i> using Docker-compose. 
But if necessary, you can change database config and secret key for JWT in .env file.
To generate a new secure random key you can use the command
<blockquote>openssl rand -hex 32</blockquote>

<h3>Launch</h3>

Install docker and docker-compose packages
<blockquote>pip install docker docker-compose</blockquote>
Run docker containers
<blockquote>docker-compose up --build</blockquote>

To start using service you have to sign up at <code>/auth/register</code> 
endpoint with body request:
<blockquote>{
    <br>"username": "AnyUsername",
    <br>"password": "123"
<br>}
</blockquote>
<code>To sign up with ADMIN role just uncomment <i>role</i> field in <i>app/auth/router.py</i> file</code>

Then go to <code>/auth/login</code> endpoint to get access token with the same body request:
<blockquote>{
    <br>"username": "AnyUsername",
    <br>"password": "123"
<br>}
</blockquote>
The endpoint returns the access token. If you use Postman API platform you 
should pass the token to Authorization header with Type: <code>Bearer token</code>

<h3>Docs</h3>
Check full OpenAPI service documentation at <code>/docs</code> endpoint.
