# Dr. Scratch

<img width="1012" height="359" alt="Local De" src="https://github.com/user-attachments/assets/b3314297-e65a-4083-a656-6150fa33e77a" />


**Dr. Scratch** is an analysis tool that evaluates your Scratch projects across various computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelism, flow control, user interactivity, and data representation. This analyzer is useful for assessing both your own projects and those of your students.

You can try a beta version at [https://drscratch.org](https://drscratch.org).

---

## Local Deployment

Follow these steps to set up and run a local instance of Dr. Scratch.

### Prerequisites

Make sure you have the following tools installed:

- **Docker** 20.10.x or newer.
- **Docker Compose** 1.28.x or newer.

### 1. Clone the Repository

First, clone the official Dr. Scratch repository from GitHub:

```bash
git clone https://github.com/ucm-dr-scratch/drscratchv3.git
cd drscratchv3
```

### 2. Create the Environment File (`.env`)

Before starting the containers, it is **essential** to create a file named `.env` in the root of the project. This file contains all the configuration variables required for the services to communicate with each other.

#### Django Configuration

```
DRSCRATCH_DEBUG=True
DRSCRATCH_SECRET_KEY=drscratchv3
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,drscratch.org
CSRF_TRUSTED_ORIGINS=https://drscratch.org,https://www.drscratch.org
```

#### Database Configuration (MySQL)

```
DRSCRATCH_SQLENGINE=django.db.backends.mysql
DRSCRATCH_DATABASE_NAME=drscratchv3_database
DRSCRATCH_DATABASE_USER=drscratchv3
DRSCRATCH_DATABASE_PASSWORD=password
DRSCRATCH_DATABASE_ROOT_PASSWORD=password
DRSCRATCH_DATABASE_HOST=db
DRSCRATCH_DATABASE_PORT=3306
```

> **Note:** `DRSCRATCH_DATABASE_HOST` is set to `db`, which is the name of the service defined in `docker-compose.yml`.

#### Celery Configuration (RabbitMQ)

```
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
```


This is what your complete `.env` file should look like:

```
# Django Configuration
DRSCRATCH_DEBUG=True
DRSCRATCH_SECRET_KEY=drscratchv3
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,drscratch.org
CSRF_TRUSTED_ORIGINS=https://drscratch.org,https://www.drscratch.org

# Database Configuration (MySQL)
DRSCRATCH_SQLENGINE=django.db.backends.mysql
DRSCRATCH_DATABASE_NAME=drscratchv3_database
DRSCRATCH_DATABASE_USER=drscratchv3
DRSCRATCH_DATABASE_PASSWORD=password
DRSCRATCH_DATABASE_ROOT_PASSWORD=password
DRSCRATCH_DATABASE_HOST=db
DRSCRATCH_DATABASE_PORT=3306

# Celery Configuration (RabbitMQ)
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Email Configuration (Batch Mode and Contact Form)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# reCAPTCHA Configuration (Contact Form)
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
```

### 3. Build and Start the Containers

Once the `.env` file is created, open a terminal in the root of the project and run:

```
docker-compose build
docker-compose up
```

After a few moments, the application will be available at [http://localhost:8000](http://localhost:8000).

---

## Additional Feature Configuration

Some features, such as batch analysis (`Batch Mode`) and the contact form, require additional configuration in the `.env` file.

### Email Sending (Batch Mode and Contact Form)

To allow Dr. Scratch to send emails, you need to configure an SMTP provider. Add the following to your `.env` file:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_password_or_app_password
EMAIL_USE_TLS=True
```

> **Tip for Gmail:** It is recommended to generate an **application-specific password** instead of using your main password. You can do this from your Google account security settings.

### reCAPTCHA (Contact Form)

To protect the contact form from spam, Google reCAPTCHA is used. You will need to obtain your own keys from [https://www.google.com/recaptcha/admin](https://www.google.com/recaptcha/admin). Then add the following to your `.env` file:

```
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
```

---

## Application Management with `make`

The `Makefile` includes several helpful commands for managing the development environment:

- `make build`: Builds or rebuilds container images.
- `make start`: Starts all services in the background.
- `make stop`: Stops and removes all containers.
- `make celery-restart`: Restarts the Celery service if needed.
- `make translate`: Compiles the application's translation files.
- `make static`: Runs `collectstatic` inside the Django container.

---

## Container Management

### Accessing the Containers

To access the command line of a running container:

```
docker exec -it container_name bash
```

---

## Translations

To compile the application’s translation files, run:

```
python manage.py compilemessages
```


---

## 📚 Selected Publications

- **Dr. Scratch: A Web Tool to Automatically Evaluate Scratch Projects**  
  *Jesús Moreno-León, Gregorio Robles*  
  *Proceedings of the Workshop in Primary and Secondary Computing Education (WiPSCE '15)*  
  [DOI: 10.1145/2818314.2818338](https://doi.org/10.1145/2818314.2818338)  
  This poster paper introduces Dr. Scratch, a gamified web tool designed to automatically analyze Scratch projects and assess computational thinking skills. It also identifies common programming issues among novice learners.

---

- **CT4ALL: Towards Putting Teachers in the Loop to Advance Automated Computational Thinking Metric Assessments in Game-Based Learning**  
  *Giovanni M. Troiano, Michael Cassidy, Daniel Escobar Morales, Guillermo Pons, Amir Abdollahi, Gregorio Robles, Gillian Puttick, Casper Harteveld*  
  *Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems (CHI '25)*  
  [DOI: 10.1145/3706598.3713368](https://doi.org/10.1145/3706598.3713368)  
  This work extends Dr. Scratch to support more robust CT assessments in game-based learning (GBL), integrating teacher feedback to improve metric design and usability in STEM education.

---

- **3D-Printed Models as a Prelude: Enhancing Comprehension of VR Software City Visualizations**  
  [SSRN Preprint (2025)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5207717#paper-references-widget)  
  This research explores the use of 3D-printed models to enhance user understanding before transitioning to virtual reality visualizations of software cities, bridging tangible and immersive representations.

---


