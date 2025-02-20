# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Unreleased
- add support for KB filtering capability to Bedrock Agent Target.
