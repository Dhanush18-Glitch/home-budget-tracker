# Home Budget Expense Tracker and Analysis System

## Abstract

This project provides a local Flask application for manually recording household income and expenses, grouping records by category, setting monthly category budgets, and examining savings and spending patterns. It turns a scattered personal record into a queryable database and a set of explainable summaries and charts.

## Problem and objectives

Households often know individual purchases but cannot quickly calculate monthly expenses, savings, category contributions, or budget overruns. The system records transactions with a date, type, category, amount, description, and optional payment method. It calculates totals and budget indicators from stored records rather than fixed dashboard values.

The objectives are to implement valid income/expense CRUD, category and budget management, reproducible descriptive analysis, exports, and a clear local interface that a B.Tech student can explain during a viva.

## Scope and boundaries

One trusted local user enters financial records manually. The project supports records, filters, budgets, reports, and charts. It does not connect to banks or payment gateways, process payments, store banking credentials, forecast markets, recommend investments, or provide multi-user authentication.

## Requirements

Functional requirements: transaction CRUD; default and custom categories; monthly budgets; over-budget detection; dashboard KPIs; analytics; four charts; CSV exports; health check; and JSON APIs. Non-functional requirements: responsive pages, decimal amounts, environment-based configuration, safe validation, database constraints, idempotent seeding, and testable services.

## Architecture and stack

Browser templates and JSON clients call Flask blueprints. Routes use validation and service modules, which use SQLAlchemy models with MySQL as the production target and SQLite only as a local demo/test option. Pandas and NumPy operate on records retrieved from the database. Matplotlib writes generated chart images. The stack is Python, Flask, SQLAlchemy, MySQL/PyMySQL, Pandas, NumPy, Matplotlib, Jinja2, HTML/CSS, and pytest.

## Plan, outcomes, and limitations

The project follows schema and model design, CRUD and validation, analytics and charts, automated tests, then documentation and a live demonstration. Expected outcomes are a demonstrable local workflow and repeatable sample data. The approved listing calls the project Beginner while its detailed specification labels Project 8 Intermediate; this implementation follows the detailed intermediate scope. MySQL deployment requires a locally configured server and was not available for verification in this workspace.
