# 0125 Spring, SpringBoot

## Spring

: Java 기반의 애플리케이션 프레임워크로 **엔터프라이즈급 애플리케이션(**기업 환경을 대상으로 하는 개발)을 개발하기 위한 다양한 기능을 제공

### **특징**

- **제어 역전 (Inversion of Control)**
    - 객체의 관리를 컨테이너에 맡겨 제어권이 넘어간 것
    - 기존 자바 개발 방식과 달리, 사용할 객체를 직접 생성하지 않고 객체의 생명 주기 관리를 외부(Spring Container, IoC Container)에 위임.
    - 제어 역전을 통해 DI, AOP 가능

- **의존성 주입 (Dependency Injection)**
    - 제어 역전의 방법 중 하나로, 사용할 객체를 직접 생성하지 않고 외부 컨테이너가 생성한 객체를 주입받아 사용하는 방식
    - `@Autowired`을 통해 의존성을 주입
    
    ```jsx
    **Spring 의존성 주입 방법**
    1. 생성자
    2. 필드 객체 선언
    3. setter 메소드
    ```
    
- **관점 지향 프로그래밍 (Aspect Oriented Programming)**
    - 핵심 기능과 부가 기능으로 구분하고, 관점을 기준으로 묶어 개발하는 방식
    
    ---
    
- **어노테이션**
    - @Controller, @Service, @Repository, @Component, @Configuration : 스프링 컨테이너에서 빈을 등록
    - @Autowired, @Value, @Transactional: 스프링부트의 DI
    AOP 등 다양한 기능 구현
    
- **빈(Bean)**
    - 스프링 컨테이너에서 생성되고 관리되는 객체
        - 특징
            - DI, AOP 지원
            - 높은 가독성과 유지보수성
        

---

### **레이어드 아키텍처**

: 애플리케이션을 계층으로 나누어 설계하는 방법

- **프레젠테이션 계층 (UI 계층)**
    - 애플리케이션의 최상단 계층
    - 클라이언트의 요청을 해석하고 응답하는 역할
    - UI나 API를 제공
    - 비즈니스 계층으로 요청을 위임하고 받은 결과를 응답
    
- **비즈니스 계층 (Service 계층)**
    - 애플리케이션이 제공하는 기능을 정의
    - 세부 작업을 수행하는 도메인 객체를 통해 업무를 위임
    - Domain-Driven Design 기반의 아키텍처에서는 비즈니스 로직에 도메인이 포함되기도 하고, 별도로 도메인 계층을 두기도 함

- **데이터 접근 계층 (Persistance 계층)**
    - 데이터베이스에 접근하는 일련의 작업 수행
    

---

### **DAO와 DTO**

- 주로  Layered Architecture에서 사용
- 애플리케이션의 구조와 유지 보수성을 높이는 데 중요한 역할

- **DAO : Data Access Object**
    - DB와 통신하여 데이터를 읽고 쓰는 데 사용
    - 데이터 접근 계층(Data Access Layer)에서 사용
    - 애플리케이션의 비즈니스 로직과 데이터베이스 간의 인터페이스 역할을 수행
    - 데이터베이스에 대한 모든 접근이 이루어진다
    - Repository와 같은 개념으로 사용되기도 함
    - Spring Boot는 JPA와 함께 사용될 때, DAO 대신 Repository를 사용
- **DTO : Data Transfer Object**
    - 애플리케이션 내 객체 간 데이터 전송
    - 비즈니스 로직에서 데이터를 전달하거나, 다른 시스템으로 데이터 전송
    - Spring Boot는 JPA와 함께 사용될 때 DTO 대신 Entity를 사용
    

---

### SpringBoot에서의 레이어드 아키텍처 설계

1. **Controller Layer**
    - 웹 요청을 받아 처리하는 컨트롤러 클래스가 위치하는 패키지
    - 일반적으로 `@Controller`나 `@RestController` 어노테이션 사용
    - 주요 어노테이션
        - `@Controller`: HTTP 요청을 처리하는 컨트롤러 클래스임을 나타내며, 주로
        View를 반환
        - `@RestController`: HTTP 요청을 처리하는 RESTful 컨트롤러 클래스임을
        나타내며, JSON/XML 등의 데이터를 반환
        - `@GetMapping` / `@PostMapping` / `@PutMapping` / `@DeleteMapping`: 각각
        HTTP GET/POST/PUT/DELETE 요청에 매핑되는 메서드임을 나타내며, URL
        패턴 지정 가능
        - `@RequestBody`: HTTP 요청 본문(body)의 데이터를 객체로 매핑할 때 사용. 주로 RESTful API에서 사용
        - `@Autowired`: 필요한 객체를 자동으로 주입하도록 지정. 스프링 프레임워크에서는 IoC/DI 패턴을 사용하여 객체 간의 의존성을 관리
        
    1. **Service Layer**
        - 비즈니스 로직을 처리하는 서비스 클래스가 위치하는 패키지
        - 일반적으로 `@Service` 어노테이션 사용
        
    2. **Repository Layer**
        - 데이터베이스와 연동하여 데이터를 조회하고 조작하는 클래스가 위치하는 패키지
        - 일반적으로 `@Repository` 어노테이션 사용
        - 데이터베이스에 접근하기 위해 일반적으로 JPA나 MyBatis와 같은 ORM 프레임워크 사용
        
    3. **Model Layer**
        - 데이터를 담는 모델 클래스가 위치하는 패키지
        - 일반적으로 `@Entity` 어노테이션 사용 (.model)
        - 데이터베이스와의 매핑을 위해 일반적으로 JPA 어노테이션 사용
        - Entity의 주요 어노테이션
            - `@Entity`: JPA 엔티티 클래스임을 나타내며, 해당 클래스의 객체가
            데이터베이스에 저장될 수 있도록 설정합니다.
            - `@Table`: 데이터베이스 테이블과 매핑될 엔티티 클래스임을 나타내며,
            데이터베이스 테이블 이름을 지정할 수 있습니다.
            - `@Id`: 엔티티의 기본 키임을 나타내며, 해당 필드는 반드시 선언되어야 합니다.
            - `@GeneratedValue`: 기본 키 값을 자동으로 생성하기 위한 전략을 지정합니다.
            - `@Column`: 데이터베이스 테이블의 컬럼과 매핑될 필드임을 나타내며,
            데이터베이스 컬럼명을 지정할 수 있습니다
        - DTO의 주요 어노테이션
            - `@NoArgsConstructor`: 매개변수 없는 생성자 자동 생성
            - `@AllArgsConstructor`: 모든 매개변수를 포함하는 생성자 자동 생성
            - `@Getter`: getter 메서드를 자동 생성
            - `@Setter`: setter 메서드를 자동 생성
            - `@ToString`: 해당 클래스 toString 메서드를 자동 생성
            
    4. **Exception Layer**
        - 예외 처리를 담당하는 클래스가 위치하는 패키지
        - 일반적으로 `@ControllerAdvice` 어노테이션과 함께 사용. (.exception)