# Reflection: Development & Testing Process

## Key Experiences

- **JWT Authentication:**  
  Implemented secure registration and login endpoints using FastAPI. Passwords are hashed before storage, and JWT tokens are issued upon successful login. Pydantic schemas ensure robust validation and data integrity.

- **Front-End Integration:**  
  Developed functional registration and login pages using HTML, CSS, and JavaScript. Client-side validation checks for email format and password length, improving user experience and reducing invalid submissions. JWT tokens are stored in localStorage for authenticated requests.

- **Playwright E2E Testing:**  
  Created comprehensive end-to-end tests covering positive and negative scenarios for registration and login. Tests interact with UI elements, submit forms, and verify both UI feedback and server responses. This helped catch edge cases and ensured reliability.

- **CI/CD Pipeline:**  
  Configured GitHub Actions to automate testing and deployment. The pipeline spins up the database and server, runs all tests (unit, integration, E2E), and pushes the Docker image to Docker Hub if all checks pass. This streamlined the workflow and improved code quality.

## Challenges Faced

- **Test Data Isolation:**  
  Ensuring each E2E test uses unique user data to avoid conflicts and false positives.

- **Playwright Setup in CI:**  
  Integrating Playwright with GitHub Actions required additional setup steps (installing browsers, handling dependencies).

- **Validation Feedback:**  
  Synchronizing server-side and client-side validation messages for a consistent user experience.

- **Docker & Database Coordination:**  
  Managing service dependencies and health checks in Docker Compose and CI workflows to avoid race conditions.

## Lessons Learned

- Automated E2E testing is essential for catching UI and integration bugs early.
- A robust CI/CD pipeline saves time and ensures consistent deployments.
- Clear documentation and modular code structure make onboarding and maintenance easier.
