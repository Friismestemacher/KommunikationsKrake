# coding: utf-8

"""
    Sommerblut-Database

    Event and festival info  # noqa: E501

    OpenAPI spec version: 1.5.0
    Contact: support@xtain.net
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from sb_db.api_client import ApiClient


class LocationsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_current_location_groups(self, **kwargs):  # noqa: E501
        """get all locationsGroups from current events  # noqa: E501

        get all locationsGroups from current events with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_current_location_groups(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str accept_language: request specific language
        :return: LocationGroups
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_current_location_groups_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_current_location_groups_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_current_location_groups_with_http_info(self, **kwargs):  # noqa: E501
        """get all locationsGroups from current events  # noqa: E501

        get all locationsGroups from current events with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_current_location_groups_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str accept_language: request specific language
        :return: LocationGroups
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_current_location_groups" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'accept_language' in params:
            header_params['Accept-Language'] = params['accept_language']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/api/locationGroups/current.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LocationGroups',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_all_location_groups(self, **kwargs):  # noqa: E501
        """get all locationGroups  # noqa: E501

        get all locationGroups with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_location_groups(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str accept_language: request specific language
        :return: LocationGroups
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_location_groups_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_location_groups_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_location_groups_with_http_info(self, **kwargs):  # noqa: E501
        """get all locationGroups  # noqa: E501

        get all locationGroups with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_location_groups_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str accept_language: request specific language
        :return: LocationGroups
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_location_groups" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}
        if 'accept_language' in params:
            header_params['Accept-Language'] = params['accept_language']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/api/locationGroups.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LocationGroups',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_location_group_by_id(self, location_group_id, **kwargs):  # noqa: E501
        """Find locationGroup by ID  # noqa: E501

        Returns a single locationGroup with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_location_group_by_id(location_group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int location_group_id: ID of locationGroup to return (required)
        :param str accept_language: request specific language
        :return: LocationGroup
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_location_group_by_id_with_http_info(location_group_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_location_group_by_id_with_http_info(location_group_id, **kwargs)  # noqa: E501
            return data

    def get_location_group_by_id_with_http_info(self, location_group_id, **kwargs):  # noqa: E501
        """Find locationGroup by ID  # noqa: E501

        Returns a single locationGroup with all related locations  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_location_group_by_id_with_http_info(location_group_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int location_group_id: ID of locationGroup to return (required)
        :param str accept_language: request specific language
        :return: LocationGroup
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['location_group_id', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_location_group_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'location_group_id' is set
        if ('location_group_id' not in params or
                params['location_group_id'] is None):
            raise ValueError("Missing the required parameter `location_group_id` when calling `get_location_group_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'location_group_id' in params:
            path_params['locationGroupId'] = params['location_group_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'accept_language' in params:
            header_params['Accept-Language'] = params['accept_language']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth']  # noqa: E501

        return self.api_client.call_api(
            '/api/locationGroups/{locationGroupId}.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='LocationGroup',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
