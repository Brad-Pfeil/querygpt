# QueryGPT: NL-to-SQL Pipeline

This project implements a modular, multi-agent pipeline to convert natural language questions into SQL queries. It is designed to work with complex relational databases, making data access more intuitive and accessible.

## How It Works

Instead of relying on a single, monolithic model, this system uses a series of specialised agents that work in sequence to deconstruct a user's question and build a precise SQL query. This approach improves accuracy, reduces token usage, and makes the system easier to debug and maintain.

The pipeline consists of the following agents:

1.  **Intent Agent**: Determines the user's intent or the business domain of the query (e.g., "student management," "academic performance"). This helps narrow the search space for the subsequent steps.
2.  **Table Agent**: Selects the most relevant database tables required to answer the user's question based on the identified intent and the database schema.
3.  **Column Prune Agent**: Further refines the context by selecting only the specific columns from the chosen tables that are necessary for the query. This minimizes the prompt size and improves the final model's focus.
4.  **SQL Generator**: Takes the pruned schema, the user's query, and relevant few-shot examples (retrieved from a Neo4j vector store) to generate the final, syntactically correct SQL query.

The project uses `llama-index` for its core components, `pydantic-ai` for agent creation and validation, and a Neo4j database for vector storage to support Retrieval-Augmented Generation (RAG).

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.12+
- `uv` package manager
### 2. Installation

First, clone the repository to your local machine.

Create a virtual environment and install the required dependencies, including the project in editable mode:

```bash
# Create the virtual environment
uv venv

# Install dependencies
uv pip install -e .
```

### 3. Environment Variables

The pipeline requires API keys for OpenAI and credentials for your Neo4j database. Copy `.env` file in the root of the project directory and add the following variables:

```env
# .env
OPENAI_API_KEY=sk-...
NEO4J_URI=neo4j+s://your-neo4j-uri.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password
EMBEDDING_DIM=1536
RAG_K=3
```

Replace the placeholder values with your actual credentials.

## Example Usage

Once the setup is complete, you can run queries from your terminal. The application will automatically seed a sample SQLite database (`sample_university.db`) on its first run.

Here is an example of running a query:

```bash
uv run querygpt "How many students are in each department?"
```

### Example Output

```
--- SQL Query ---
SELECT d.name, COUNT(s.department_id) AS student_count FROM departments d LEFT JOIN students s ON d.id = s.department_id GROUP BY d.name;

--- Explanation ---
This SQL query counts the number of students in each department. It starts by selecting the department name from the 'departments' table and counting the occurrences of department IDs from the 'students' table. The LEFT JOIN ensures that departments with no students will still be included in the results, showing a count of zero for those departments. The results are grouped by the department name, which allows the count of students to be aggregated for each department.

--- Result Preview ---
{
  "name": {
    "0": "Computer Science",
    "1": "Mathematics",
    "2": "Physics"
  },
  "student_count": {
    "0": 2,
    "1": 1,
    "2": 1
  }
}
```
