"""
This is a template for creating custom ColumnExpectations.
For detailed instructions on how to use it, please see:
    https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_aggregate_expectations
"""

from typing import Dict, Optional

from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.exceptions import InvalidExpectationConfigurationError
from great_expectations.execution_engine import (
    ExecutionEngine,
    PandasExecutionEngine,
    SparkDFExecutionEngine,
    SqlAlchemyExecutionEngine,
)
from great_expectations.expectations.expectation import ColumnExpectation, ColumnMapExpectation
from great_expectations.expectations.metrics import (
    ColumnAggregateMetricProvider,
    column_aggregate_partial,
    column_aggregate_value,
    column_condition_partial,
    ColumnMapMetricProvider
)

#from textblob import TextBlob 
from spellchecker import SpellChecker
spell = SpellChecker()

# This class defines a Metric to support your Expectation.
# For most ColumnExpectations, the main business logic for calculation will live in this class.
class ColumnValuesCorrectSpelling(ColumnMapMetricProvider): #(ColumnMapMetricProvider):#

    # This is the id string that will be used to reference your Metric.
    condition_metric_name = "column_values.correct_spelling"

    # This method implements the core logic for the PandasExecutionEngine
    @column_condition_partial(engine=PandasExecutionEngine)
    def _pandas(cls, column, **kwargs):
        
        # logic implementation:        
        def check_spelling(text):
            
            text = [text]
            x = len(spell.unknown(text)) == 0
                
            return x
        
        return column.apply(check_spelling) # return boolean array

    # This method defines the business logic for evaluating your Metric when using a SqlAlchemyExecutionEngine
    # @column_aggregate_partial(engine=SqlAlchemyExecutionEngine)
    # def _sqlalchemy(cls, column, _dialect, **kwargs):
    #     raise NotImplementedError
    #
    # This method defines the business logic for evaluating your Metric when using a SparkDFExecutionEngine
    # @column_aggregate_partial(engine=SparkDFExecutionEngine)
    # def _spark(cls, column, **kwargs):
    #     raise NotImplementedError


# This class defines the Expectation itself
class ExpectColumnValuesToBeSpeltCorrectly(ColumnMapExpectation):
    
    """Expect string values in a column to be spelt correctly."""

    # These examples will be shown in the public gallery.
    # They will also be executed as unit tests for your Expectation.
    
    examples = [
        {
            "data": {"x": ['this', 'sentence', 'is', 'spelt', 'correctly'], "y": ['this', 'sentnence', 'not', 'splet', 'corectly']},
            "tests": [
                {
                    "title": "basic_positve_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "x"},
                    "out": {"success": True},
                },
                {
                    "title": "basic_nagative_test",
                    "exact_match_out": False,
                    "include_in_gallery": True,
                    "in": {"column": "y", "mostly": 1},
                    "out": {"success": False},
                }
            ]
        }
    ]

    # This is a tuple consisting of all Metrics necessary to evaluate the Expectation.
    #metric_dependencies = ("column_values.correct_spelling",)
    map_metric = "column_values.correct_spelling"

    # This a tuple of parameter names that can affect whether the Expectation evaluates to True or False.
    success_keys = ("mostly",)

    # This dictionary contains default values for any parameters that should have default values.
    default_kwarg_values = {}

    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration]
    ) -> None:
        """
        Validates that a configuration has been set, and sets a configuration if it has yet to be set. Ensures that
        necessary configuration arguments have been provided for the validation of the expectation.
        Args:
            configuration (OPTIONAL[ExpectationConfiguration]): \
                An optional Expectation Configuration entry that will be used to configure the expectation
        Returns:
            None. Raises InvalidExpectationConfigurationError if the config is not validated successfully
        """

        super().validate_configuration(configuration)
        if configuration is None:
            configuration = self.configuration

        # # Check other things in configuration.kwargs and raise Exceptions if needed
        # try:
        #     assert (
        #         ...
        #     ), "message"
        #     assert (
        #         ...
        #     ), "message"
        # except AssertionError as e:
        #     raise InvalidExpectationConfigurationError(str(e))

    # This object contains metadata for display in the public Gallery
    library_metadata = {
        "tags": [],  # Tags for this Expectation in the Gallery
        "contributors": [  # Github handles for all contributors to this Expectation.
            "@your_name_here",  # Don't forget to add your github handle here!
        ],
        "requirements": ["pyspellchecker"]
    }


if __name__ == "__main__":    
    ExpectColumnValuesToBeSpeltCorrectly().print_diagnostic_checklist()