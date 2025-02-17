from pathlib import Path
import tomli


CFG_MAP: dict[str, str] = {
	'test': 'test.toml',
}


def _get_cfg_path(cfile: str):
	# depending where we are (local, docker, installed) cfg
	# can be in a different place.
	cfg = Path('/conf/conf.toml')
	if cfg.exists():
		return cfg

	cfg_path = Path(__file__).parent.parent.parent.parent / 'conf' / cfile
	cpath: Path = Path(cfg_path)
	if not cpath.exists():
		raise Exception(f'Bad configuration path {cfg_path=}')
	return cpath


def _blocking_load_cfg(cpath: Path) -> 'AppCfg':
	with cpath.open(mode='rb') as fp:
		app_cfg = AppCfg(tomli.load(fp))
	return app_cfg


class AppCfg(dict):

	@classmethod
	def from_env(cls, env: str) -> 'AppCfg':
		cfile: str = CFG_MAP.get(env)
		if cfile is None:
			raise Exception(f'no config found: {env}')

		cpath = _get_cfg_path(cfile)
		app_cfg = _blocking_load_cfg(cpath)  # BLOCKS, but we cant do much before cfg loaded
		return app_cfg
