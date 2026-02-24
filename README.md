## Baseline python backend project

### minimal agents.md instructions:
 - tech stack
 - project structure
 - code style and conventions
 - things should not do

### Typical Project Structure

```
src/
├── controllers/    (UserController) handle HTTP requests using Controller pattern for MVC
├── services/       (UserService) encapsulate business logic, often implementing the Service Layer pattern
├── repositories/   (IUserRepository interface and UserRepository impl) abstract db operations via the Repository pattern, decoupling data access from business logic
├── models/         Models or Entities (User class) represent domain objects, aligning with Domain Driven Design
├── middlewares/    (AuthMiddleware) apply cross-cutting concerns like the Chain of Responsibility pattern
└── config/
```

1. Controllers / Handlers (Entry Point)
This module manages the interface between the web and the application logic.
Common Class Names: UserController, ProductHandler, AuthResolver.
Design Patterns:
Proxy: The controller acts as a proxy, forwarding requests to internal services.
Adapter: Converts incoming HTTP/JSON data into internal Domain Objects or DTOs.
Command: In CQRS (Command Query Responsibility Segregation) architectures, controllers turn requests into "Command" objects.

2. Services / Use Cases (Business Logic)
This is the core of the project where the "rules" of the application live.
Common Class Names: PaymentService, OrderProcessor, EnrollUserUseCase.
Design Patterns:
Facade: Services provide a simple interface to complex underlying logic or multiple repositories.
Strategy: Used when you have multiple ways to perform a task (e.g., PaypalStrategy vs. StripeStrategy).
Template Method: Defines the skeleton of an algorithm (e.g., an export process) while letting subclasses implement specific steps.

3. Domain Models / Entities (The "Truth")
These classes represent the data structures and the logic directly related to them.
Common Class Names: User, Invoice, Transaction.
Design Patterns:
Domain Model: Objects that encapsulate both data and behavior.
Data Transfer Object (DTO): Simple classes used only to move data between layers (no logic).
Factory: Used to instantiate complex entities (e.g., UserFactory.createAdmin()).

4. Repositories / DAOs (Data Access)
This module abstracts the database technology away from the business logic.
Common Class Names: UserRepository, ProductDao, OrderMapper.
Design Patterns:
Repository Pattern: Mediates between the domain and data mapping layers, acting like an in-memory collection.
Data Mapper: Moves data between objects and a database while keeping them independent.
Singleton: Often used for database connection pools to ensure only one instance exists.

5. Middleware / Interceptors (Cross-Cutting Concerns)
Logic that runs before or after the main processing (logging, auth, error handling).
Common Class Names: AuthGuard, LoggingInterceptor, ErrorHandler.
Design Patterns:
Chain of Responsibility: Requests pass through a "chain" of middleware; each can either process the request or pass it to the next link.
Decorator: Dynamically adds behavior to a function or class without modifying its code.

6. Infrastructure / Clients (External Systems)
Handles communication with third-party APIs, message brokers, or file systems.
Common Class Names: S3Client, EmailGateway, KafkaProducer.
Design Patterns:
Adapter: Wraps a third-party SDK to match your application's internal interface.
Observer: Used with message brokers (like RabbitMQ) where the system "observes" events and reacts.
