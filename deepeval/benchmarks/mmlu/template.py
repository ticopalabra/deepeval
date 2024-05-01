from deepeval.benchmarks.mmlu.task import MMLUTask


class MMLUTemplate:

    # Most of this template was taken from MMLU Github Repo
    # The output confinement is a novel addition, since the original code
    # outputted log_probabilties for each answer choice

    @staticmethod
    def generate_output(
        input: str, train_set: object, task: MMLUTask, n_shots: int
    ):
        if n_shots > 0: 
            prompt = "The following are {} multiple choice example questions (with answers) about{}, followed by the actual question that you need to answer to.\n\n"
        else:
            prompt = ""
        prompt = prompt.format(n_shots-1, MMLUTemplate.format_subject(task.value))
        for i in range(n_shots):
            example = i<n_shots-1
            prompt += MMLUTemplate.format_question(train_set[i], include_answer=example)
        prompt += input

        # define ouptut confinement
        #prompt += "Output 'A', 'B', 'C', or 'D'. Full answer not needed."
        prompt += "\nAnswer to this question only 'A', 'B', 'C', or 'D'. Don't provide any further comments or explanation as this will invalidate the answer. "
        return prompt

    @staticmethod
    def format_question(data: dict, include_answer: bool = True):
        prompt = data["input"]
        choices = ["A", "B", "C", "D"]
        for j in range(len(choices)):
            choice = choices[j]
            prompt += "\n{}. {}".format(choice, data[choice])
        
        if include_answer:
            prompt += "\nAnswer:"
            prompt += " {}\n\n".format(data["target"])
        return prompt

    def format_subject(subject: str):
        l = subject.split("_")
        s = ""
        for entry in l:
            s += " " + entry
        return s
