from distutils.core import setup, Extension


def main():
	ensemble_mod = Extension('ensemble',['ensemble.cpp'],None)

	setup( name = "ensemble_mod",
		version ="1.0",
		description = " test extension",
		ext_modules = [ensemble_mod],
	)
if __name__ == '__main__':
	main()
