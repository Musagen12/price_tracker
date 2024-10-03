# Price Tracker Project 🛒✨

Welcome to the **Price Tracker Project**! This project is aimed at scraping product data from Jumia, an online marketplace, and storing it in a structured database. 

## 📅 Ongoing Development

This project is currently **ongoing**. We're continuously improving the functionality, performance, and adding new features! Your feedback and contributions are welcome! 

## 🚀 Features

- **Dynamic Table Creation**: Automatically creates tables in the database based on product UUIDs.
- **Product Data Scraping**: Efficiently scrapes product details from Jumia and Amazon.
- **Automated Task Scheduling**: Uses Celery to automate scraping tasks every 20 minutes.
- **Asynchronous Processing**: Utilizes async functions for concurrent URL processing, speeding up data retrieval.
- **Comment analysis using llms**: Analyzes the comments using llms.

## 🛠️ Technologies Used

- **FastAPI**: For building the web application and API.
- **SQLAlchemy**: For database interactions.
- **Selenium and Selenium-wire**: For browser automation.
- **Requests-html**: For getting specific data.
- **Celery**: For task scheduling.
- **Redis**: As a message broker for Celery.
- **Asyncio**: For handling asynchronous operations.
- **Langchain**: For interacting with the llm.
- **Chroma**: For creating a vector database for the llm to query.
- **Ollama**: For running llms "locally".

## 📦 Installation

- **Comming soon**

## 🌟 Contributing

We welcome contributions! Feel free to fork the repo and submit a pull request. If you have suggestions or issues, please open an issue on GitHub.

## 📬 Contact

For questions or suggestions, please raise an issue.

## 📄 License

This project is licensed under the MIT License.
