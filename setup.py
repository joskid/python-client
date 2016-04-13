from setuptools import setup
from setuptools.command.test import test as TestCommand

with open('README.rst', 'r') as f:
  readme = f.read()


def strip_requirement(line):
  # skip blank lines or comments
  if not line or line.startswith('#'):
    return
  return line.strip()

with open('requirements.txt', 'r') as f:
  requirements = [strip_requirement(x) for x in f if strip_requirement(x)]

with open('requirements-dev.txt', 'r') as f:
  test_requirements = [strip_requirement(x) for x in f if strip_requirement(x)]

# We can't just import the module and pull out __version__, because the module
# won't be installed yet *while* this is being installed.
with open('handwritingio/version.py', 'r') as f:
  version = 'unknown'
  for line in f:
    line = line.strip()
    if line.startswith('__version__ = '):
      version = line.lstrip('__version__ = ').strip("'").strip('"')
      break


class Tox(TestCommand):
  user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

  def initialize_options(self):
    TestCommand.initialize_options(self)
    self.tox_args = None

  def finalize_options(self):
    TestCommand.finalize_options(self)
    self.test_args = []
    self.test_suite = True

  def run_tests(self):
    # import here, cause outside the eggs aren't loaded
    import tox
    import shlex
    args = self.tox_args
    if args:
        args = shlex.split(self.tox_args)
    errno = tox.cmdline(args=args)
    sys.exit(errno)


setup(
  name='handwritingio',
  version=version,
  description='Handwriting.io API client.',
  long_description=readme,
  author='Handwriting.io',
  author_email='support@handwriting.io',
  url='https://github.com/handwritingio/python-client',
  classifiers=(
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ),
  packages=['handwritingio'],
  license='MIT License',
  install_requires=requirements,
  tests_require=['tox'],
  cmdclass = {'test': Tox},
)
