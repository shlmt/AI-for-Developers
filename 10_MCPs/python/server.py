from fastmcp import FastMCP
import csv

mcp = FastMCP(name="bmi-analyzer")

@mcp.tool
def calc_bmi(height: float, weight: float) -> float:
    """
    Calculate BMI for person.
    heignt in cm, weight in kg.
    """
    return round(weight / (height / 100) ** 2, 2)

@mcp.resource("knowledge://bmi_table")
def get_table(): 
    return {
        "underweight": "BMI < 18.5",
        "normal": "18.5 <= BMI < 25",
        "overweight": "25 <= BMI < 30",
        "obese": "BMI >= 30"
    }

@mcp.resource("users://{user_id}/profile")
def get_details(user_id: int):
    with open("persons.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["user_id"]) == user_id:
                return {
                    "height": float(row["height_cm"]),
                    "weight": float(row["weight_kg"]),
                    "gender": row["gender"],
                    "age": int(row["age"])
                }
    return {}

@mcp.prompt
def summarize_request(text: str) -> str:
    """Generate a prompt asking for BMI interpretation."""
    return (
        "Analyze the BMI data below and provide a medical interpretation based on age, gender, height, and weight.\n"
        f"\n{text}\n"
    )

mcp.run("stdio")
