import argparse
import os
from src.config.config import Configuration
from src.input.input import InputModule
from src.api.api_calls import APIModule
from src.ner.ner import NERModule
from src.prevalence.prevalence import PrevalenceModule
from src.explanation.explanation import ExplanationModule


def run_experiment():
    parser = argparse.ArgumentParser(description='A program that executes the explanation quality assesment pipeline.')

    # Add arguments
    parser.add_argument('-i', '--individual_run', type=bool, help='Pass True to avoid batch runs')
    parser.add_argument('-m', '--transformer_model', help='The huggingface model name for the NER finetunning model')
    parser.add_argument('-e', '--epochs', type=int, help='Number of epochs for the finetunning')
    parser.add_argument('-t', '--threshold', type=float, help='Threshold to compute the tuples.txt intermediate dataset')
    parser.add_argument('-d', '--destination_path', help='Path to the directory in which models, reports, etc will be stored')

    # Parse the arguments
    args = parser.parse_args()

    # Create module instances
    config = Configuration(transformer=args.transformer_model, threshold=args.threshold, epochs=args.epochs)
    input_module = InputModule()
    api_module = APIModule()
    prevalence_module = PrevalenceModule()
    explanation_module = ExplanationModule()
    
    
    if args.individual_run:
        #TO DO : sacar referencias extra a threshold
        print(1)
        ner_module = NERModule(args.transformer_model, args.threshold, config=config)

        # Read input file
        input_data = input_module.read_input_file()
        print(2)
        # Perform NER
        if config.run_ner:
            ner_module.perform_ner(input_data)
        print(3)
        if config.run_matches_finetuning:
            ner_module.finetune_tuples()
        print(4)
        # Make API calls
        if config.run_onthology_matching:
            api_module.make_api_calls()

        # Calculate prevalence
        #prevalence_value = prevalence_module.calculate_prevalence(api_response)

        # Generate explanation
        #explanation_text = explanation_module.generate_explanation(prevalence_value, named_entities)
    else:
        for transformer in config.transformers_list:
            for threshold in config.thresholds_list:
                ner_module = NERModule(transformer, threshold)

                # Read input file
                input_data = input_module.read_input_file()

                # Perform NER
                if config.run_ner:
                    ner_module.perform_ner(input_data)

                if config.run_matches_finetuning:
                    ner_module.finetune_tuples()

                # Make API calls
                if config.run_onthology_matching:
                    api_module.make_api_calls()

                # Calculate prevalence
                #prevalence_value = prevalence_module.calculate_prevalence(api_response)

                # Generate explanation
                #explanation_text = explanation_module.generate_explanation(prevalence_value, named_entities)

run_experiment()
