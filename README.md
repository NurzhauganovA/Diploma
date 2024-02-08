# School Management System

This project is aimed at developing an internal school management system that can be used by different schools, whether they work with our system or not. The system provides functionality for registration, user profile management, school creation, contract management, parent and student registration, class management, payment processing, report generation, subject, club, and section management, attendance tracking, and grading. Additional features can be added as per the requirements of the user.

## Features

1. **Registration and User Management**: Users can register as school administrators. After registration, users can edit their profiles.

2. **School Creation**: School administrators can create their own schools. The administrator can be a director, manager, or assistant director. After creating a school, the administrator will have the role of "Administrator" and will be linked to the created school.

3. **Dashboard**: The dashboard displays data about the selected school, including the number of students, parents, and teachers, the total amount of contracts, and the total amount of contract debts.

4. **Contract Creation and Management**: The system allows administrators to register parents with specific data. Parents can register their children and apply for school admission. Administrators can also register children and link them to specific parents. Administrators can create classes and assign students to classes. Contracts are created with a unique number and a date until May 25th. Each school has a fixed contract amount and payment type. The payment type is for the year, and the contract amount for the year is divided into 9 months. Payment by parents is calculated as the monthly amount divided by the number of days in the month. In case of a student's illness, the payment for the days of illness is canceled, and there is a recalculation of the monthly amount. Payments can be processed offline.

5. **Reports**: Reports are generated from contracts. Monthly reports show contract numbers and their data, as well as all payments for the month. Debt reports show contracts with debts. The system also has reports on subjects, clubs, and sections. Reports can be filtered by the accountant to select specific months, for example, September and October, and show contracts with debts for these months.

6. **Subjects, Clubs, and Sections**: Each student can have multiple subjects, clubs, and sections for the year. Each student has their own schedule. Subjects have their own grading and attendance systems.

## Installation

1. Clone the repository: `git clone https://github.com/NurzhauganovA/Diploma.git`
2. Open Docker directory: `cd docker/prod`
3. Docker compose: `docker compose -f docker-compose-prod.yml up --build`

## Usage

1. Register as a school administrator.
2. Create your school and manage its details.
3. Manage contracts, including parent and student registration and class management.
4. Process payments and generate reports.
5. Manage subjects, clubs, and sections for students.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your suggestions or improvements.
