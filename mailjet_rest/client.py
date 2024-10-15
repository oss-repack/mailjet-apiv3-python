#!/usr/bin/env python
from __future__ import annotations

import json
import logging
import re
from typing import AnyStr
from re import Match

import requests
from requests.compat import urljoin
from requests.models import Response

from .utils.version import get_version

requests.packages.urllib3.disable_warnings()


def prepare_url(key: Match[str]) -> str:
    """Replaces capital letters to lower one with dash prefix."""
    char_elem = key.group(0)
    if char_elem.isupper():
        return "-" + char_elem.lower()
    return ""


class Config:
    DEFAULT_API_URL = "https://api.mailjet.com/"
    API_REF = "http://dev.mailjet.com/email-api/v3/"
    version = "v3"
    user_agent = "mailjet-apiv3-python/v" + get_version()

    def __init__(self, version: str | None = None, api_url: str | None = None):
        if version is not None:
            self.version = version
        self.api_url = api_url or self.DEFAULT_API_URL

    def __getitem__(self, key: str) -> tuple[AnyStr, dict[str, str]]:
        # Append version to URL.
        # Forward slash is ignored if present in self.version.
        url = urljoin(self.api_url, self.version + "/")
        headers = {"Content-type": "application/json", "User-agent": self.user_agent}
        if key.lower() == "contactslist_csvdata":
            url = urljoin(url, "DATA/")
            headers["Content-type"] = "text/plain"
        elif key.lower() == "batchjob_csverror":
            url = urljoin(url, "DATA/")
            headers["Content-type"] = "text/csv"
        elif key.lower() != "send" and self.version != "v4":
            url = urljoin(url, "REST/")
        url = url + key.split("_")[0].lower()
        return url, headers


class Endpoint:
    def __init__(
        self,
        url: str,
        headers: dict[str, str],
        auth: tuple[str, str],
        action: str | None = None,
    ) -> None:
        self._url, self.headers, self._auth, self.action = url, headers, auth, action

    def _get(
        self,
        filters: dict[str, str | int | float] | None = None,
        action_id: str | None = None,
        id: str | None = None,
        **kwargs,  # type: ignore
    ) -> Response:
        return api_call(
            self._auth,
            "get",
            self._url,
            headers=self.headers,
            action=self.action,
            action_id=action_id,
            filters=filters,
            resource_id=id,
            **kwargs,
        )

    def get_many(
        self,
        filters: dict[str, str | int | float] | None = None,
        action_id: str | None = None,
        **kwargs,  # type: ignore
    ) -> Response:
        return self._get(filters=filters, action_id=action_id, **kwargs)

    def get(
        self,
        id: str | None = None,
        filters: dict[str, str | int | float] | None = None,
        action_id: str | None = None,
        **kwargs,  # type: ignore
    ) -> Response:
        return self._get(id=id, filters=filters, action_id=action_id, **kwargs)

    def create(
        self,
        data: dict | None = None,
        filters: dict[str, str | int | float] | None = None,
        id: str | None = None,
        action_id: str | None = None,
        ensure_ascii: bool = True,
        data_encoding: str = "utf-8",
        **kwargs,
    ) -> Response:
        if self.headers["Content-type"] == "application/json":
            if ensure_ascii:
                data = json.dumps(data)
            else:
                data = json.dumps(data, ensure_ascii=False).encode(data_encoding)
        return api_call(
            self._auth,
            "post",
            self._url,
            headers=self.headers,
            resource_id=id,
            data=data,
            action=self.action,
            action_id=action_id,
            filters=filters,
            **kwargs,  # type: ignore
        )

    def update(
        self,
        id: str | None,
        data: bytes,
        filters: dict[str, str | int | float] | None = None,
        action_id: str | None = None,
        ensure_ascii: bool = True,
        data_encoding: str = "utf-8",
        **kwargs,
    ) -> Response:
        if self.headers["Content-type"] == "application/json":
            if ensure_ascii:
                data = json.dumps(data)
            else:
                data = json.dumps(data, ensure_ascii=False).encode(data_encoding)
        return api_call(
            self._auth,
            "put",
            self._url,
            resource_id=id,
            headers=self.headers,
            data=data,
            action=self.action,
            action_id=action_id,
            filters=filters,
            **kwargs,  # type: ignore
        )

    def delete(self, id: str | None, **kwargs) -> Response:
        return api_call(
            self._auth,
            "delete",
            self._url,
            action=self.action,
            headers=self.headers,
            resource_id=id,
            **kwargs,  # type: ignore
        )


class Client:
    def __init__(self, auth: tuple[str, str] | None = None, **kwargs) -> None:
        self.auth = auth
        version = kwargs.get("version")
        api_url = kwargs.get("api_url")
        self.config = Config(version=version, api_url=api_url)

    def __getattr__(self, name: str):
        name = re.sub(r"[A-Z]", prepare_url, name)
        split = name.split("_")
        # identify the resource
        fname = split[0]
        action = None
        if len(split) > 1:
            # identify the sub resource (action)
            action = split[1]
            if action == "csvdata":
                action = "csvdata/text:plain"
            if action == "csverror":
                action = "csverror/text:csv"
        url, headers = self.config[name]
        return type(fname, (Endpoint,), {})(
            url=url, headers=headers, action=action, auth=self.auth
        )


def api_call(
    auth: tuple[str, str],
    method: str | None,
    url: str,
    headers: dict[str, str],
    data: dict | None = None,
    filters: dict[str, str | int | float] | None = None,
    resource_id: str | None = None,
    timeout: int = 60,
    debug: bool = False,
    action: str | None = None,
    action_id: str | None = None,
    **kwargs,  # type: ignore
) -> Response:
    url = build_url(
        url, method=method, action=action, resource_id=resource_id, action_id=action_id
    )
    req_method = getattr(requests, method)

    try:
        filters_str = None
        if filters:
            filters_str = "&".join(f"{k}={v}" for k, v in filters.items())
        response = req_method(
            url,
            data=data,
            params=filters_str,
            headers=headers,
            auth=auth,
            timeout=timeout,
            verify=True,
            stream=False,
        )
        return response

    except requests.exceptions.Timeout as e:
        raise TimeoutError from e
    except requests.RequestException as e:
        raise ApiError from e
    except Exception:
        raise


def build_headers(
    resource: str, action: str | None = None, extra_headers: dict | None = None
) -> dict[str, str]:
    """Build headers based on resource and action."""
    headers = {"Content-type": "application/json"}

    if resource.lower() == "contactslist" and action.lower() == "csvdata":
        headers = {"Content-type": "text/plain"}
    elif resource.lower() == "batchjob" and action.lower() == "csverror":
        headers = {"Content-type": "text/csv"}

    if extra_headers:
        headers.update(extra_headers)

    return headers


def build_url(
    url: str,
    method: str | None,
    action: str | None = None,
    resource_id: str | None = None,
    action_id: str | None = None,
) -> str:
    if action:
        url += f"/{action}"
        if action_id:
            url += f"/{action_id}"
    if resource_id:
        url += f"/{resource_id!s}"
    return url


def parse_response(response: Response, debug: bool = False) -> dict:
    data = response.json()

    if debug:
        logging.debug("REQUEST: %s" % response.request.url)
        logging.debug("REQUEST_HEADERS: %s" % response.request.headers)
        logging.debug("REQUEST_CONTENT: %s" % response.request.body)

        logging.debug("RESPONSE: %s" % response.content)
        logging.debug("RESP_HEADERS: %s" % response.headers)
        logging.debug("RESP_CODE: %s" % response.status_code)

    return data


class ApiError(Exception):
    pass


class AuthorizationError(ApiError):
    pass


class ActionDeniedError(ApiError):
    pass


class CriticalApiError(ApiError):
    pass


class ApiRateLimitError(ApiError):
    pass


class TimeoutError(ApiError):
    pass


class DoesNotExistError(ApiError):
    pass


class ValidationError(ApiError):
    pass
