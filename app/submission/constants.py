# Language
LANG_C = 0
LANG_CPP = 1
LANG_RUBY = 2
LANG_PHP = 3
LANG_JAVA = 4
LANG_PYTHON = 5

LANGUAGES = {
	LANG_C: 'C',
	LANG_CPP: 'C++',
	LANG_RUBY: 'Ruby',
	LANG_PHP: 'PHP',
	LANG_JAVA: 'Java',
	LANG_PYTHON: 'Python'
}

LANG_EXTENSIONS = {
	LANG_C: 'c',
	LANG_CPP: 'cpp',
	LANG_RUBY: 'rb',
	LANG_PHP: 'php',
	LANG_JAVA: 'java',
	LANG_PYTHON: 'py',
}

LANG_PARAMS_MAPPING = {
	LANG_C: 'c',
	LANG_CPP: 'c++',
	LANG_RUBY: 'ruby',
	LANG_PHP: 'php',
	LANG_JAVA: 'java',
	LANG_PYTHON: 'python',
}

# state
STATE_QUEUED = 'queued'
STATE_FINISHED = 'finished'

# result status
RESULT_TIME_EXCEEDED = 'Limited time exceeded'
RESULT_MEMORY_EXCEEDED = 'Limited memory exceeded'
RESULT_COMPILE_ERROR = 'Compile Error'
RESULT_RUNTIME_ERROR = 'Runtime Error'
RESULT_WRONG_ANSWER = 'Wrong Answer'
RESULT_ACCEPTED = 'Accepted'