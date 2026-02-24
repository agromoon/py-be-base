## Baseline python backend project

### minimal agents.md instructions:
 - tech stack
 - project structure
 - code style and conventions
 - things should not do

 ### typical project structure:
   src/
|----controllers/   (UserController) handle HTTP requests using Controller pattern for MVC.
|----services/      (UserService) encapsulate business logic, often implementing the Service Layer pattern.
|----repositories/  (IUserRepository interface and UserRepository impl) abstract db operations via the Repository pattern, decoupling data access from business logic.
|----models/        Models or Entities (User class) represent domain objects, aligning with Domain Driven Design.
|----middlewares/   (AuthMiddleware) apply cross-cutting concerns like the Chain of Responsibility pattern.
|----config/
