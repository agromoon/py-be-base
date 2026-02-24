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

#### 1. Controllers / Handlers (Entry Point)
This module manages the interface between the web and the application logic.<br>
*Common Class Names:* UserController, ProductHandler, AuthResolver.<br>
*Design Patterns:*<br>
*Proxy:* The controller acts as a proxy, forwarding requests to internal services.<br>
*Adapter:* Converts incoming HTTP/JSON data into internal Domain Objects or DTOs.<br>
*Command:* In CQRS (Command Query Responsibility Segregation) architectures, controllers turn requests into "Command" objects.<br>

#### 2. Services / Use Cases (Business Logic)
This is the core of the project where the "rules" of the application live.<br>
*Common Class Names:* PaymentService, OrderProcessor, EnrollUserUseCase.<br>
*Design Patterns:*<br>
*Facade:* Services provide a simple interface to complex underlying logic or multiple repositories.<br>
*Strategy:* Used when you have multiple ways to perform a task (e.g., PaypalStrategy vs. StripeStrategy).<br>
*Template Method:* Defines the skeleton of an algorithm (e.g., an export process) while letting subclasses implement specific steps.<br>

#### 3. Repositories / DAOs (Data Access)
This module abstracts the database technology away from the business logic.<br>
*Common Class Names:* UserRepository, ProductDao, OrderMapper.<br>
*Design Patterns:*<br>
*Repository Pattern:* Mediates between the domain and data mapping layers, acting like an in-memory collection.<br>
*Data Mapper:* Moves data between objects and a database while keeping them independent.<br>
*Singleton:* Often used for database connection pools to ensure only one instance exists.<br>

#### 4. Domain Models / Entities (The "Truth")
These classes represent the data structures and the logic directly related to them.<br>
*Common Class Names:* User, Invoice, Transaction.<br>
*Design Patterns:*<br>
*Domain Model:* Objects that encapsulate both data and behavior.<br>
*Data Transfer Object (DTO):* Simple classes used only to move data between layers (no logic).<br>
*Factory:* Used to instantiate complex entities (e.g., UserFactory.createAdmin()).<br>

#### 5. Middleware / Interceptors (Cross-Cutting Concerns)
Logic that runs before or after the main processing (logging, auth, error handling).<br>
*Common Class Names:* AuthGuard, LoggingInterceptor, ErrorHandler.<br>
*Design Patterns:*<br>
*Chain of Responsibility:* Requests pass through a "chain" of middleware; each can either process the request or pass it to the next link.<br>
*Decorator:* Dynamically adds behavior to a function or class without modifying its code.<br>

#### 6. Infrastructure / Clients (External Systems)
Handles communication with third-party APIs, message brokers, or file systems.<br>
*Common Class Names:* S3Client, EmailGateway, KafkaProducer.<br>
*Design Patterns:*<br>
*Adapter:* Wraps a third-party SDK to match your application's internal interface.<br>
*Observer:* Used with message brokers (like RabbitMQ) where the system "observes" events and reacts.
