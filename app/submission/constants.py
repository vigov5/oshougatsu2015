# Language
LANG_C = 0
LANG_CPP = 1
LANG_RUBY = 2
LANG_PHP = 3
LANG_JAVA = 4
LANG_PYTHON = 5
LANG_GO = 6
LANG_JAVASCRIPT = 7
LANG_PERL = 8

LANGUAGES = {
	LANG_C: 'C',
	LANG_CPP: 'C++',
	LANG_RUBY: 'Ruby 1.9',
	LANG_PHP: 'PHP 5.5',
	LANG_JAVA: 'Java 7',
	LANG_PYTHON: 'Python 2.7',
	LANG_GO: 'Go 1.2',
	LANG_JAVASCRIPT: 'JavaScript (NodeJS 0.10)',
	LANG_PERL: 'Perl 5.18'
}

LANG_EXTENSIONS = {
	LANG_C: 'c',
	LANG_CPP: 'cpp',
	LANG_RUBY: 'rb',
	LANG_PHP: 'php',
	LANG_JAVA: 'java',
	LANG_PYTHON: 'py',
	LANG_GO: 'go',
	LANG_JAVASCRIPT: 'js',
	LANG_PERL: 'pl'
}

LANG_PARAMS_MAPPING = {
	LANG_C: 'c',
	LANG_CPP: 'c++',
	LANG_RUBY: 'ruby',
	LANG_PHP: 'php',
	LANG_JAVA: 'java',
	LANG_PYTHON: 'python',
	LANG_GO: 'go',
	LANG_JAVASCRIPT: 'javascript',
	LANG_PERL: 'perl'
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