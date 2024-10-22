# Recommender

## Overview

The Recommender is a CLI application that will provide job recommendations to job seekers based on their skills and the required skills for each job.  

The application will have two inputs:  jobs.csv and jobseekers.csv.  

`jobseekers.csv`: This file contains information about jobseekers. Each row represents a jobseeker and has the following columns:

* `id`: A unique identifier for the jobseeker.
* `name`: The name of the jobseeker.
* `skills`: A comma-separated list of the jobseeker's skills.

```
id,name,skills
1,Alice Seeker,"Ruby, SQL, Problem Solving"
2,Bob Applicant,"JavaScript, HTML/CSS, Teamwork"
3,Charlie Jobhunter,"Java, SQL, Problem Solving"
...
```

`jobs.csv`: This file contains information about jobs. Each row represents a job and has the following columns:

* `id`: A unique identifier for the job.
* `title`: The title of the job.
* `required_skills`: A comma-separated list of skills required for the job.

```
id,title,required_skills
1,Ruby Developer,"Ruby, SQL, Problem Solving"
2,Frontend Developer,"JavaScript, HTML/CSS, React, Teamwork"
3,Backend Developer,"Java, SQL, Node.js, Problem Solving"
...
```

Matches will contain the number matching skills and the matching percentage.  Matching percentage is computed as matched_count / required_skills_count.

Below is a sample output of the application:

```
jobseeker_id, jobseeker_name, job_id, job_title, matching_skill_count, matching_skill_percent
1, Alice, 5, Ruby Developer, 3, 100
1, Alice, 2, .NET Developer, 3, 75
1, Alice, 7, C# Developer, 3, 75
1, Alice, 4, Dev Ops Engineer, 4, 50
2, Bob, 3, C++ Developer, 4, 100
2, Bob, 1, Go Developer, 3, 75
...
```

The outputs can be sent either to the terminal or to a csv file depending on the provided parameters to the application.

## Details

When matching between jobseekers and jobs, an inverted index is created in memory for the jobs based on skills.  This was done to help
facilitate the matching and avoid expensive looping through the whole list of jobs.  This comes with a trade off however that Memory use for this application
will be higher the more records there are in the jobs.csv.

Initial testing has shown that for a file of 1000 rows of jobs, it can perform matching for as much as XXX jobseekers with total execution time of YYYY

Other design decisions were:

- The application was written using [Click](https://click.palletsprojects.com/en/8.1.x/#) to facilitate flexibility in handling inputs and their validation.
- linting used ruff - facilitate clean code
- formatting used black - facilitate uniform formatting
- testing used pytest and pytest-cov - ensure quality and code coverage
- logging used structlog - use JSON renderer for logs out of the box

## Development

### Project Structure

```
recommender/
│
├── build/                 # Build artifacts
├── data/                  # Data files (e.g., CSVs)
├── logs/                  # Log files
├── src/                   # Source code
│   ├── recommender/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── commands.py
│   │   ├── constants.py
│   │   ├── input.py
│   │   ├── logging_config.py
│   │   ├── models.py
│   │   └── services.py
├── tests/                 # Unit tests
├── LICENSE                # License file
├── README.md              # This file
└── pyproject.toml         # Project metadata and dependencies
```


### Installation

Dependencies for the project is configured on pyproject.toml.  

To install the project, ensure that you have python 3.12 and do below:

```bash
git clone https://github.com/junsilva/recommender.git
cd recommender
python -m venv .venv
source .venv/scripts/activate
pip install .[dev]
```

### Running

After installing, recommend script should be callable now.  

You can launch the application by using recommend like below or by calling the recommender python module

```bash
$ recommend
```

```
$ python -m recommender
```

## Debugging / Running in VS Code:

You can run and debug the application using below sample run configuration:

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run recommender -- Terminal output",
            "type": "debugpy",
            "request": "launch",
            "module": "recommender",
            "console": "integratedTerminal",
            "args": [
                "csv-input",
                "${input:jobseeker_path}",
                "${input:job_path}"
            ]
        },
        {
            "name": "Run recommender -- File output",
            "type": "debugpy",
            "request": "launch",
            "module": "recommender",
            "console": "integratedTerminal",
            "args": [
                "csv-input",
                "${input:jobseeker_path}",
                "${input:job_path}",
                "--output",
                "${input:output_file}"
            ]
        }        
    ],
    "inputs": [
        {
            "id": "jobseeker_path",
            "type": "promptString",
            "description": "Enter jobseeker csv file"
        },
        {
            "id": "job_path",
            "type": "promptString",
            "description": "Enter job csv file"
        },
        {
            "id": "output_file",
            "type": "promptString",
            "description": "Enter output csv file"
        },        
    ]
}

```

### Testing

Tests can be run using tox.

```
$ tox
```

Coverage is currently at ~90%


## Improvements

Of the top of my head, below are improvements that can be done

[ ] Refine unit tests for generating files.  
[ ] refine logging to use queue handlers.
[ ] implement chunking of jobs to handle larger datasets


## License

This project is licensed under the MIT License - see the LICENSE file for details.