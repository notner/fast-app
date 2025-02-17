from pathlib import Path
import tomli

from defaultapp.lib import exc


CFG_MAP: dict[str, str] = {
	'local': 'local.toml',
	'prod': 'prod.toml',
	'stg': 'stg.toml',
	'test': 'test.toml',
}


class AppCfg(dict):

	@classmethod
	def from_env(cls, env: str) -> 'AppCfg':
		cfile: str = CFG_MAP.get(env)
		if cfile is None:
			raise exc.ConfigException(f'no config found: {env}')
		cfg_path = Path(__file__).parent.parent.parent.parent / 'conf' / cfile

		cpath: Path = Path(cfg_path)
		if not cpath.exists():
			raise exc.ConfigException(f'Bad configuration path {cfg_path=}')

		with cpath.open(mode='rb') as fp:
			app_cfg = AppCfg(tomli.load(fp))

		return app_cfg
