from adaptix import Retort

dcf = Retort()

dcf_load = dcf.load
dcf_dump = dcf.dump

__all__ = (
    'dcf',
    'dcf_load',
    'dcf_dump',
)
