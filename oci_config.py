""" Hysun He (hysun.he@oracle.com) @ 2023/07/04 """
import oci


class OciConf:
    """ docstring """
    _CONFIG_PATH = '~/.oci/config'
    _OCI_CONF = None
    _NAMESPACE = None

    @classmethod
    def oci_config(cls):
        """ docstring """
        if cls._OCI_CONF is None:
            cls._OCI_CONF = oci.config.from_file(
                file_location=cls._CONFIG_PATH)
        return cls._OCI_CONF

    @classmethod
    def core_client(cls):
        """ docstring """
        return oci.core.ComputeClient(cls.oci_config())

    @classmethod
    def object_storage_client(cls):
        """ docstring """
        return oci.object_storage.ObjectStorageClient(cls.oci_config())

    @classmethod
    def get_region(cls):
        """ docstring """
        return cls.oci_config()['region']  #pylint: disable=unsubscriptable-object

    @classmethod
    def get_namespace(cls):
        """ docstring """
        if cls._NAMESPACE is None:
            response = cls.object_storage_client().get_namespace(
                compartment_id=cls.oci_config()['tenancy'])  #pylint: disable=unsubscriptable-object
            cls._NAMESPACE = response.data
        return cls._NAMESPACE
