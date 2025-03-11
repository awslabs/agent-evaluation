# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0]

### Added
- Added support to use any Anthropic or Meta Foundation Model and request configuration with the evaluator
- Added a default Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude Haiku 3.5, and Meta Llama3.3 configuration
- Added `src/agenteval/evaluators/model_config/` to define above default configurations as well as the interface in the code
- Added `src/agenteval/evaluators/bedrock_request/bedrock_request_handler.py` to handle differences in Bedrock request/response shapes across providers
- Added `samples/test_plan_templates/bedrock_agent_target/vary_eval_llm_example/` folder with samples of new model selection functionality
- Added support to optionally specify the file name for the test plan YAML, defaulting to `agenteval.yml` in `Plan.load`
- Added documentation to page about evaluators reflecting changes

### Changed
- Renamed `src/agenteval/evaluators/claude3` -> `src/agenteval/evaluators/canonical`
- Renamed `src/agenteval/templates/evaluators/claude3` -> `src/agenteval/templates/evaluators/canonical`

## [0.3.0]

### Added
- Added pass rate metric to summary ([#60](https://github.com/awslabs/agent-evaluation/pull/60))
- Added support of session attributes for bedrock agent target([#77] (https://github.com/awslabs/agent-evaluation/pull/77))
- Added Target for Prompt Flows ([#96](https://github.com/awslabs/agent-evaluation/pull/96))

### Fixed
- Bedrock agent required arguments documented as optional ([#92](https://github.com/awslabs/agent-evaluation/pull/92))
- Fix test result attribute in summary template ([#90](https://github.com/awslabs/agent-evaluation/pull/90))

### Changed
- Renamed `TestResult.success` to `TestResult.passed` ([#62](https://github.com/awslabs/agent-evaluation/pull/62))
- Moved `agenteval.TargetResponse` to `agenteval.targets.TargetResponse`. Documentation for creating custom targets also updated to reflect this change ([#62](https://github.com/awslabs/agent-evaluation/pull/62))
- Renamed the target config `type` from `bedrock-knowledgebase` to `bedrock-knowledge-base` ([#62](https://github.com/awslabs/agent-evaluation/pull/62))

## [0.2.0] - 2024-05-13

### Changed
- Convert the `q_business_user_id` configuration as optional to support applications that require AWS IAM Identity Center ([#56](https://github.com/awslabs/agent-evaluation/pull/56))
- Changed `TargetResponse` to a top-level import ([#57](https://github.com/awslabs/agent-evaluation/pull/57))

### Fixed
- Documentation for creating custom targets ([#57](https://github.com/awslabs/agent-evaluation/pull/57))

## [0.1.0] - 2024-05-03

### Added
- Initial release
