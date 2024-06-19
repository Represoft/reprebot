#!/bin/sh
set -e

# Run the context builder scripts
cd src/context_builder/faculty_secretary_faq && python main.py
cd ../../..
cd src/context_builder/faculty_secretary_students_requests && python main.py
cd ../../..
cd src/scripts && python setup_vector_store.py
cd ../..
cd src/api

# Execute the command passed to the script
exec "$@"
