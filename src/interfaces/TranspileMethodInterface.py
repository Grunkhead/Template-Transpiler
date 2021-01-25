from abc import ABC, abstractmethod

# Inherit, Abstract Base Class
class TranspileMethodInterface(ABC):

    # Return array with conditions like: template.is_partial that return to true or false.
    # If a single condition is false, the method will not be executed for that template.
    @abstractmethod
    def exclude(template) -> [bool]: raise NotImplementedError

    # This method is used to define a single purpose transpilation.
    # For example; delete all comments from a template file.
    @abstractmethod
    def execute(template, comparison_template): raise NotImplementedError