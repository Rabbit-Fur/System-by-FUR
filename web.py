from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/project-info", methods=["POST"])
def project_info():
    try:
        data = request.get_json()
        project_id = data.get("projectId")
        environment_id = data.get("environmentId")
        token = data.get("token")

        query = """
        query GetProject($projectId: String!, $environmentId: String!) {
          project(id: $projectId) {
            id
            name
            environments(filter: {id: $environmentId}) {
              id
              name
            }
          }
        }
        """

        response = requests.post(
            "https://backboard.railway.app/graphql/v2",
            headers={
                "Project-Access-Token": token,
                "Content-Type": "application/json"
            },
            json={"query": query, "variables": {
                "projectId": project_id,
                "environmentId": environment_id
            }}
        )

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
