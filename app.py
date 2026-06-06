import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def run_crud_operations():
    try:
        # Initialize the Supabase Client
        print("Connecting to Supabase database...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Success: Connected to Supabase!\n")

        # ----------------------------------------------------------------------
        # SETUP / CLEANUP PREVIOUS RUNS
        # ----------------------------------------------------------------------
        # To make this script easily repeatable without running into duplicate key violations,
        # we clean up any pre-existing records for ID 101 and Dept ID 1 first.
        supabase.table("students").delete().eq("student_id", 101).execute()
        supabase.table("departments").delete().eq("dept_id", 1).execute()

        # ----------------------------------------------------------------------
        # STEP 1: CREATE (Insert Department Record)
        # ----------------------------------------------------------------------
        print("Step 1: Inserting department record...")
        department_record = {
            "dept_id": 1,
            "department_name": "Computer Science"
        }
        
        dept_response = supabase.table("departments").insert(department_record).execute()
        
        # Check if insertion was successful
        if dept_response.data:
            inserted_dept = dept_response.data[0]
            print(f"Success: Department '{inserted_dept['department_name']}' created successfully (ID: {inserted_dept['dept_id']}).\n")
        else:
            raise Exception("Failed to insert department record.")

        # ----------------------------------------------------------------------
        # STEP 2: CREATE (Insert Student Record)
        # ----------------------------------------------------------------------
        print("Step 2: Inserting student record...")
        student_record = {
            "student_id": 101,
            "name": "Alice Johnson",
            "age": 40,
            "department": "Computer Science",
            "marks": 90
        }
        
        student_response = supabase.table("students").insert(student_record).execute()
        
        if student_response.data:
            inserted_student = student_response.data[0]
            print(f"Success: Student '{inserted_student['name']}' created successfully (ID: {inserted_student['student_id']}).\n")
        else:
            raise Exception("Failed to insert student record.")

        # ----------------------------------------------------------------------
        # STEP 3: UPDATE (Update Student's Marks from 72 to 82)
        # ----------------------------------------------------------------------
        print("Step 3: Updating student marks from 72 to 82...")
        update_data = {
            "marks": 82
        }
        
        update_response = supabase.table("students").update(update_data).eq("student_id", 101).execute()
        
        if update_response.data:
            updated_student = update_response.data[0]
            print(f"Success: Updated student '{updated_student['name']}' marks to {updated_student['marks']}.\n")
        else:
            raise Exception("Failed to update student marks.")

        # ----------------------------------------------------------------------
        # STEP 4: READ (Retrieve the Student Record)
        # ----------------------------------------------------------------------
        print("Step 4: Reading student record from database...")
        
        read_response = supabase.table("students").select("*").eq("student_id", 101).execute()
        
        if read_response.data:
            student_data = read_response.data[0]
            print("Success: Student record successfully retrieved from database.\n")
        else:
            raise Exception("Student record not found in database.")

        # ----------------------------------------------------------------------
        # STEP 5: DISPLAY (Print the retrieved record in a clean, readable format)
        # ----------------------------------------------------------------------
        print("Step 5: Student Details (Clean Format):")
        print("=" * 40)
        print(f"  Student ID : {student_data['student_id']}")
        print(f"  Name       : {student_data['name']}")
        print(f"  Age        : {student_data['age']}")
        print(f"  Department : {student_data['department']}")
        print(f"  Marks      : {student_data['marks']}")
        print("=" * 40)
        print()

        # ----------------------------------------------------------------------
        # STEP 6: DELETE (Remove Student Record from database)
        # ----------------------------------------------------------------------
        print("Step 6: Deleting student record from database...")
        
        delete_response = supabase.table("students").delete().eq("student_id", 101).execute()
        
        if delete_response.data:
            deleted_student = delete_response.data[0]
            print(f"Success: Student '{deleted_student['name']}' (ID: {deleted_student['student_id']}) was successfully deleted.\n")
        else:
            raise Exception("Failed to delete student record.")

        # Optional: Delete the department record to keep the database completely clean
        supabase.table("departments").delete().eq("dept_id", 1).execute()
        print("Cleanup: Temporary department record deleted from database.\n")

        # ----------------------------------------------------------------------
        # FINAL SUMMARY
        # ----------------------------------------------------------------------
        print("*" * 50)
        print("SUCCESS: ALL CRUD OPERATIONS COMPLETED SUCCESSFULLY!")
        print("*" * 50)

    except Exception as error:
        print(f"\nError encountered during execution: {error}")

if __name__ == "__main__":
    run_crud_operations()