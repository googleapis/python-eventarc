# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials             # type: ignore
from google.auth.transport import mtls                            # type: ignore
from google.auth.transport.grpc import SslCredentials             # type: ignore
from google.auth.exceptions import MutualTLSChannelError          # type: ignore
from google.oauth2 import service_account                         # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.eventarc_v1.services.eventarc import pagers
from google.cloud.eventarc_v1.types import channel
from google.cloud.eventarc_v1.types import channel as gce_channel
from google.cloud.eventarc_v1.types import channel_connection
from google.cloud.eventarc_v1.types import channel_connection as gce_channel_connection
from google.cloud.eventarc_v1.types import eventarc
from google.cloud.eventarc_v1.types import trigger
from google.cloud.eventarc_v1.types import trigger as gce_trigger
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EventarcTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import EventarcGrpcTransport
from .transports.grpc_asyncio import EventarcGrpcAsyncIOTransport


class EventarcClientMeta(type):
    """Metaclass for the Eventarc client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """
    _transport_registry = OrderedDict()  # type: Dict[str, Type[EventarcTransport]]
    _transport_registry["grpc"] = EventarcGrpcTransport
    _transport_registry["grpc_asyncio"] = EventarcGrpcAsyncIOTransport

    def get_transport_class(cls,
            label: str = None,
        ) -> Type[EventarcTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class EventarcClient(metaclass=EventarcClientMeta):
    """Eventarc allows users to subscribe to various events that are
    provided by Google Cloud services and forward them to supported
    destinations.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "eventarc.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            EventarcClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            EventarcClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(
            filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EventarcTransport:
        """Returns the transport used by the client instance.

        Returns:
            EventarcTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def channel_path(project: str,location: str,channel: str,) -> str:
        """Returns a fully-qualified channel string."""
        return "projects/{project}/locations/{location}/channels/{channel}".format(project=project, location=location, channel=channel, )

    @staticmethod
    def parse_channel_path(path: str) -> Dict[str,str]:
        """Parses a channel path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/channels/(?P<channel>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def channel_connection_path(project: str,location: str,channel_connection: str,) -> str:
        """Returns a fully-qualified channel_connection string."""
        return "projects/{project}/locations/{location}/channelConnections/{channel_connection}".format(project=project, location=location, channel_connection=channel_connection, )

    @staticmethod
    def parse_channel_connection_path(path: str) -> Dict[str,str]:
        """Parses a channel_connection path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/channelConnections/(?P<channel_connection>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def cloud_function_path(project: str,location: str,function: str,) -> str:
        """Returns a fully-qualified cloud_function string."""
        return "projects/{project}/locations/{location}/functions/{function}".format(project=project, location=location, function=function, )

    @staticmethod
    def parse_cloud_function_path(path: str) -> Dict[str,str]:
        """Parses a cloud_function path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/functions/(?P<function>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def service_path() -> str:
        """Returns a fully-qualified service string."""
        return "*".format()

    @staticmethod
    def parse_service_path(path: str) -> Dict[str,str]:
        """Parses a service path into its component segments."""
        m = re.match(r"^*$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def service_account_path(project: str,service_account: str,) -> str:
        """Returns a fully-qualified service_account string."""
        return "projects/{project}/serviceAccounts/{service_account}".format(project=project, service_account=service_account, )

    @staticmethod
    def parse_service_account_path(path: str) -> Dict[str,str]:
        """Parses a service_account path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/serviceAccounts/(?P<service_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def trigger_path(project: str,location: str,trigger: str,) -> str:
        """Returns a fully-qualified trigger string."""
        return "projects/{project}/locations/{location}/triggers/{trigger}".format(project=project, location=location, trigger=trigger, )

    @staticmethod
    def parse_trigger_path(path: str) -> Dict[str,str]:
        """Parses a trigger path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/triggers/(?P<trigger>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str, ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(billing_account=billing_account, )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str,str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str, ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder, )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str,str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str, ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization, )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str,str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str, ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project, )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str,str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str, ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(project=project, location=location, )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str,str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[client_options_lib.ClientOptions] = None):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError("Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`")
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError("Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`")

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (use_mtls_endpoint == "auto" and client_cert_source):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Union[str, EventarcTransport, None] = None,
            client_options: Optional[client_options_lib.ClientOptions] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the eventarc client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, EventarcTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(client_options)

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError("client_options.api_key and credentials are mutually exclusive")

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, EventarcTransport):
            # transport is a EventarcTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError("When providing a transport instance, "
                                 "provide its credentials directly.")
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(google.auth._default, "get_api_key_credentials"):
                credentials = google.auth._default.get_api_key_credentials(api_key_value)

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def get_trigger(self,
            request: Union[eventarc.GetTriggerRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> trigger.Trigger:
        r"""Get a single trigger.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_get_trigger():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.GetTriggerRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_trigger(request=request)

                # Handle response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.GetTriggerRequest, dict]):
                The request object. The request message for the
                GetTrigger method.
            name (str):
                Required. The name of the trigger to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.types.Trigger:
                A representation of the trigger
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.GetTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.GetTriggerRequest):
            request = eventarc.GetTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_trigger]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_triggers(self,
            request: Union[eventarc.ListTriggersRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListTriggersPager:
        r"""List triggers.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_list_triggers():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.ListTriggersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_triggers(request=request)
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.ListTriggersRequest, dict]):
                The request object. The request message for the
                ListTriggers method.
            parent (str):
                Required. The parent collection to
                list triggers on.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.services.eventarc.pagers.ListTriggersPager:
                The response message for the ListTriggers method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.ListTriggersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.ListTriggersRequest):
            request = eventarc.ListTriggersRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_triggers]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListTriggersPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_trigger(self,
            request: Union[eventarc.CreateTriggerRequest, dict] = None,
            *,
            parent: str = None,
            trigger: gce_trigger.Trigger = None,
            trigger_id: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Create a new trigger in a particular project and
        location.



        .. code-block::

            from google.cloud import eventarc_v1

            def sample_create_trigger():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                trigger = eventarc_v1.Trigger()
                trigger.name = "name_value"
                trigger.event_filters.attribute = "attribute_value"
                trigger.event_filters.value = "value_value"
                trigger.destination.cloud_run.service = "service_value"
                trigger.destination.cloud_run.region = "region_value"

                request = eventarc_v1.CreateTriggerRequest(
                    parent="parent_value",
                    trigger=trigger,
                    trigger_id="trigger_id_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.create_trigger(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.CreateTriggerRequest, dict]):
                The request object. The request message for the
                CreateTrigger method.
            parent (str):
                Required. The parent collection in
                which to add this trigger.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger (google.cloud.eventarc_v1.types.Trigger):
                Required. The trigger to create.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            trigger_id (str):
                Required. The user-provided ID to be
                assigned to the trigger.

                This corresponds to the ``trigger_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, trigger, trigger_id])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.CreateTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.CreateTriggerRequest):
            request = eventarc.CreateTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if trigger is not None:
                request.trigger = trigger
            if trigger_id is not None:
                request.trigger_id = trigger_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_trigger]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gce_trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_trigger(self,
            request: Union[eventarc.UpdateTriggerRequest, dict] = None,
            *,
            trigger: gce_trigger.Trigger = None,
            update_mask: field_mask_pb2.FieldMask = None,
            allow_missing: bool = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Update a single trigger.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_update_trigger():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.UpdateTriggerRequest(
                    validate_only=True,
                )

                # Make the request
                operation = client.update_trigger(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.UpdateTriggerRequest, dict]):
                The request object. The request message for the
                UpdateTrigger method.
            trigger (google.cloud.eventarc_v1.types.Trigger):
                The trigger to be updated.
                This corresponds to the ``trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to be updated; only fields explicitly
                provided are updated. If no field mask is provided, all
                provided fields in the request are updated. To update
                all fields, provide a field mask of "*".

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            allow_missing (bool):
                If set to true, and the trigger is not found, a new
                trigger will be created. In this situation,
                ``update_mask`` is ignored.

                This corresponds to the ``allow_missing`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([trigger, update_mask, allow_missing])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.UpdateTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.UpdateTriggerRequest):
            request = eventarc.UpdateTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if trigger is not None:
                request.trigger = trigger
            if update_mask is not None:
                request.update_mask = update_mask
            if allow_missing is not None:
                request.allow_missing = allow_missing

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_trigger]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("trigger.name", request.trigger.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gce_trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_trigger(self,
            request: Union[eventarc.DeleteTriggerRequest, dict] = None,
            *,
            name: str = None,
            allow_missing: bool = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Delete a single trigger.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_delete_trigger():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.DeleteTriggerRequest(
                    name="name_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.delete_trigger(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.DeleteTriggerRequest, dict]):
                The request object. The request message for the
                DeleteTrigger method.
            name (str):
                Required. The name of the trigger to
                be deleted.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            allow_missing (bool):
                If set to true, and the trigger is
                not found, the request will succeed but
                no action will be taken on the server.

                This corresponds to the ``allow_missing`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.eventarc_v1.types.Trigger` A
                representation of the trigger resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, allow_missing])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.DeleteTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.DeleteTriggerRequest):
            request = eventarc.DeleteTriggerRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if allow_missing is not None:
                request.allow_missing = allow_missing

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_trigger]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            trigger.Trigger,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_channel(self,
            request: Union[eventarc.GetChannelRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> channel.Channel:
        r"""Get a single Channel.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_get_channel():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.GetChannelRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_channel(request=request)

                # Handle response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.GetChannelRequest, dict]):
                The request object. The request message for the
                GetChannel method.
            name (str):
                Required. The name of the channel to
                get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.types.Channel:
                A representation of the Channel
                resource. A Channel is a resource on
                which event providers publish their
                events. The published events are
                delivered through the transport
                associated with the channel. Note that a
                channel is associated with exactly one
                event provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.GetChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.GetChannelRequest):
            request = eventarc.GetChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_channel]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_channels(self,
            request: Union[eventarc.ListChannelsRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListChannelsPager:
        r"""List channels.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_list_channels():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.ListChannelsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_channels(request=request)
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.ListChannelsRequest, dict]):
                The request object. The request message for the
                ListChannels method.
            parent (str):
                Required. The parent collection to
                list channels on.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.services.eventarc.pagers.ListChannelsPager:
                The response message for the ListChannels method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.ListChannelsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.ListChannelsRequest):
            request = eventarc.ListChannelsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_channels]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListChannelsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_channel(self,
            request: Union[eventarc.CreateChannelRequest, dict] = None,
            *,
            parent: str = None,
            channel: gce_channel.Channel = None,
            channel_id: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Create a new channel in a particular project and
        location.



        .. code-block::

            from google.cloud import eventarc_v1

            def sample_create_channel():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                channel = eventarc_v1.Channel()
                channel.pubsub_topic = "pubsub_topic_value"
                channel.name = "name_value"
                channel.provider = "provider_value"

                request = eventarc_v1.CreateChannelRequest(
                    parent="parent_value",
                    channel=channel,
                    channel_id="channel_id_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.create_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.CreateChannelRequest, dict]):
                The request object. The request message for the
                CreateChannel method.
            parent (str):
                Required. The parent collection in
                which to add this channel.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel (google.cloud.eventarc_v1.types.Channel):
                Required. The channel to create.
                This corresponds to the ``channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_id (str):
                Required. The user-provided ID to be
                assigned to the channel.

                This corresponds to the ``channel_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.eventarc_v1.types.Channel` A representation of the Channel resource.
                   A Channel is a resource on which event providers
                   publish their events. The published events are
                   delivered through the transport associated with the
                   channel. Note that a channel is associated with
                   exactly one event provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, channel, channel_id])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.CreateChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.CreateChannelRequest):
            request = eventarc.CreateChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if channel is not None:
                request.channel = channel
            if channel_id is not None:
                request.channel_id = channel_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_channel_]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gce_channel.Channel,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def update_channel(self,
            request: Union[eventarc.UpdateChannelRequest, dict] = None,
            *,
            channel: gce_channel.Channel = None,
            update_mask: field_mask_pb2.FieldMask = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Update a single channel.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_update_channel():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.UpdateChannelRequest(
                    validate_only=True,
                )

                # Make the request
                operation = client.update_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.UpdateChannelRequest, dict]):
                The request object. The request message for the
                UpdateChannel method.
            channel (google.cloud.eventarc_v1.types.Channel):
                The channel to be updated.
                This corresponds to the ``channel`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to be updated; only fields explicitly
                provided are updated. If no field mask is provided, all
                provided fields in the request are updated. To update
                all fields, provide a field mask of "*".

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.eventarc_v1.types.Channel` A representation of the Channel resource.
                   A Channel is a resource on which event providers
                   publish their events. The published events are
                   delivered through the transport associated with the
                   channel. Note that a channel is associated with
                   exactly one event provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([channel, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.UpdateChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.UpdateChannelRequest):
            request = eventarc.UpdateChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if channel is not None:
                request.channel = channel
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_channel]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("channel.name", request.channel.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gce_channel.Channel,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_channel(self,
            request: Union[eventarc.DeleteChannelRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Delete a single channel.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_delete_channel():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.DeleteChannelRequest(
                    name="name_value",
                    validate_only=True,
                )

                # Make the request
                operation = client.delete_channel(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.DeleteChannelRequest, dict]):
                The request object. The request message for the
                DeleteChannel method.
            name (str):
                Required. The name of the channel to
                be deleted.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.eventarc_v1.types.Channel` A representation of the Channel resource.
                   A Channel is a resource on which event providers
                   publish their events. The published events are
                   delivered through the transport associated with the
                   channel. Note that a channel is associated with
                   exactly one event provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.DeleteChannelRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.DeleteChannelRequest):
            request = eventarc.DeleteChannelRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_channel]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            channel.Channel,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def get_channel_connection(self,
            request: Union[eventarc.GetChannelConnectionRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> channel_connection.ChannelConnection:
        r"""Get a single ChannelConnection.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_get_channel_connection():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.GetChannelConnectionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_channel_connection(request=request)

                # Handle response
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.GetChannelConnectionRequest, dict]):
                The request object. The request message for the
                GetChannelConnection method.
            name (str):
                Required. The name of the channel
                connection to get.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.types.ChannelConnection:
                A representation of the
                ChannelConnection resource. A
                ChannelConnection is a resource which
                event providers create during the
                activation process to establish a
                connection between the provider and the
                subscriber channel.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.GetChannelConnectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.GetChannelConnectionRequest):
            request = eventarc.GetChannelConnectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_channel_connection]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_channel_connections(self,
            request: Union[eventarc.ListChannelConnectionsRequest, dict] = None,
            *,
            parent: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListChannelConnectionsPager:
        r"""List channel connections.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_list_channel_connections():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.ListChannelConnectionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_channel_connections(request=request)
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.ListChannelConnectionsRequest, dict]):
                The request object. The request message for the
                ListChannelConnections method.
            parent (str):
                Required. The parent collection from
                which to list channel connections.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.eventarc_v1.services.eventarc.pagers.ListChannelConnectionsPager:
                The response message for the ListChannelConnections
                method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.ListChannelConnectionsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.ListChannelConnectionsRequest):
            request = eventarc.ListChannelConnectionsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_channel_connections]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListChannelConnectionsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_channel_connection(self,
            request: Union[eventarc.CreateChannelConnectionRequest, dict] = None,
            *,
            parent: str = None,
            channel_connection: gce_channel_connection.ChannelConnection = None,
            channel_connection_id: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Create a new ChannelConnection in a particular
        project and location.



        .. code-block::

            from google.cloud import eventarc_v1

            def sample_create_channel_connection():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                channel_connection = eventarc_v1.ChannelConnection()
                channel_connection.name = "name_value"
                channel_connection.channel = "channel_value"

                request = eventarc_v1.CreateChannelConnectionRequest(
                    parent="parent_value",
                    channel_connection=channel_connection,
                    channel_connection_id="channel_connection_id_value",
                )

                # Make the request
                operation = client.create_channel_connection(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.CreateChannelConnectionRequest, dict]):
                The request object. The request message for the
                CreateChannelConnection method.
            parent (str):
                Required. The parent collection in
                which to add this channel connection.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_connection (google.cloud.eventarc_v1.types.ChannelConnection):
                Required. Channel connection to
                create.

                This corresponds to the ``channel_connection`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            channel_connection_id (str):
                Required. The user-provided ID to be
                assigned to the channel connection.

                This corresponds to the ``channel_connection_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.eventarc_v1.types.ChannelConnection` A representation of the ChannelConnection resource.
                   A ChannelConnection is a resource which event
                   providers create during the activation process to
                   establish a connection between the provider and the
                   subscriber channel.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, channel_connection, channel_connection_id])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.CreateChannelConnectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.CreateChannelConnectionRequest):
            request = eventarc.CreateChannelConnectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if channel_connection is not None:
                request.channel_connection = channel_connection
            if channel_connection_id is not None:
                request.channel_connection_id = channel_connection_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_channel_connection]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gce_channel_connection.ChannelConnection,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_channel_connection(self,
            request: Union[eventarc.DeleteChannelConnectionRequest, dict] = None,
            *,
            name: str = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation.Operation:
        r"""Delete a single ChannelConnection.


        .. code-block::

            from google.cloud import eventarc_v1

            def sample_delete_channel_connection():
                # Create a client
                client = eventarc_v1.EventarcClient()

                # Initialize request argument(s)
                request = eventarc_v1.DeleteChannelConnectionRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_channel_connection(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()
                print(response)

        Args:
            request (Union[google.cloud.eventarc_v1.types.DeleteChannelConnectionRequest, dict]):
                The request object. The request message for the
                DeleteChannelConnection method.
            name (str):
                Required. The name of the channel
                connection to delete.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.eventarc_v1.types.ChannelConnection` A representation of the ChannelConnection resource.
                   A ChannelConnection is a resource which event
                   providers create during the activation process to
                   establish a connection between the provider and the
                   subscriber channel.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError('If the `request` argument is set, then none of '
                             'the individual field arguments should be set.')

        # Minor optimization to avoid making a copy if the user passes
        # in a eventarc.DeleteChannelConnectionRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, eventarc.DeleteChannelConnectionRequest):
            request = eventarc.DeleteChannelConnectionRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_channel_connection]

         # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            channel_connection.ChannelConnection,
            metadata_type=eventarc.OperationMetadata,
        )

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()



try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-eventarc",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = (
    "EventarcClient",
)
