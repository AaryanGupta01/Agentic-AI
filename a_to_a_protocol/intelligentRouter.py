# This file defines a Router class that routes tasks to different agents based on their skills.
class Router:
 
    def __init__(self):
 
        self.skills={
 
            "DockerAgent":[
                "docker",
                "container",
                "image"
            ],
 
            "K8sAgent":[
                "kubernetes",
                "k8s",
                "pod"
            ],
 
            "TerraformAgent":[
                "terraform",
                "iac",
                "infrastructure"
            ]
        }
 
    def route(self,task):
 
        scores={}
 
        task=task.lower()
 
        for agent,tags in self.skills.items():
 
            scores[agent]=sum(
                tag in task
                for tag in tags
            )
 
        return scores
 
router=Router()
 
result=router.route(
    "Deploy container image using docker"
)
 
print(result)
 
winner=max(
    result,
    key=result.get
)
 
print("Selected:",winner)