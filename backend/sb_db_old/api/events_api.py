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


class EventsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_events(self, **kwargs):  # noqa: E501
        """get all events  # noqa: E501

        get all events  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_events(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int year: returns all events of the given year<br>Example: /api/events.json?year=2020
        :param int archive: returns all events of archived or not archived festivals<br>Example: /api/events.json?archive=1
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_events_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_events_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_events_with_http_info(self, **kwargs):  # noqa: E501
        """get all events  # noqa: E501

        get all events  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_events_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int year: returns all events of the given year<br>Example: /api/events.json?year=2020
        :param int archive: returns all events of archived or not archived festivals<br>Example: /api/events.json?archive=1
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['order', 'entries', 'page', 'year', 'archive', 'category', 'tag', 'accessible', 'location', 'time', 'from_date', 'to_date', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_events" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
            collection_formats['order'] = 'multi'  # noqa: E501
        if 'entries' in params:
            query_params.append(('entries', params['entries']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'archive' in params:
            query_params.append(('archive', params['archive']))  # noqa: E501
        if 'category' in params:
            query_params.append(('category', params['category']))  # noqa: E501
            collection_formats['category'] = 'multi'  # noqa: E501
        if 'tag' in params:
            query_params.append(('tag', params['tag']))  # noqa: E501
            collection_formats['tag'] = 'multi'  # noqa: E501
        if 'accessible' in params:
            query_params.append(('accessible', params['accessible']))  # noqa: E501
            collection_formats['accessible'] = 'multi'  # noqa: E501
        if 'location' in params:
            query_params.append(('location', params['location']))  # noqa: E501
            collection_formats['location'] = 'multi'  # noqa: E501
        if 'time' in params:
            query_params.append(('time', params['time']))  # noqa: E501
            collection_formats['time'] = 'multi'  # noqa: E501
        if 'from_date' in params:
            query_params.append(('fromDate', params['from_date']))  # noqa: E501
            collection_formats['fromDate'] = 'multi'  # noqa: E501
        if 'to_date' in params:
            query_params.append(('toDate', params['to_date']))  # noqa: E501
            collection_formats['toDate'] = 'multi'  # noqa: E501

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
            '/api/events.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Events',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_current_events(self, **kwargs):  # noqa: E501
        """get all current events  # noqa: E501

        returns all published events that are not already archived  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_events(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int year: returns all events of the given year<br>Example: /api/events.json?year=2020
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_current_events_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_current_events_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_current_events_with_http_info(self, **kwargs):  # noqa: E501
        """get all current events  # noqa: E501

        returns all published events that are not already archived  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_current_events_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int year: returns all events of the given year<br>Example: /api/events.json?year=2020
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['order', 'entries', 'page', 'year', 'category', 'tag', 'accessible', 'location', 'time', 'from_date', 'to_date', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_current_events" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
            collection_formats['order'] = 'multi'  # noqa: E501
        if 'entries' in params:
            query_params.append(('entries', params['entries']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'category' in params:
            query_params.append(('category', params['category']))  # noqa: E501
            collection_formats['category'] = 'multi'  # noqa: E501
        if 'tag' in params:
            query_params.append(('tag', params['tag']))  # noqa: E501
            collection_formats['tag'] = 'multi'  # noqa: E501
        if 'accessible' in params:
            query_params.append(('accessible', params['accessible']))  # noqa: E501
            collection_formats['accessible'] = 'multi'  # noqa: E501
        if 'location' in params:
            query_params.append(('location', params['location']))  # noqa: E501
            collection_formats['location'] = 'multi'  # noqa: E501
        if 'time' in params:
            query_params.append(('time', params['time']))  # noqa: E501
            collection_formats['time'] = 'multi'  # noqa: E501
        if 'from_date' in params:
            query_params.append(('fromDate', params['from_date']))  # noqa: E501
            collection_formats['fromDate'] = 'multi'  # noqa: E501
        if 'to_date' in params:
            query_params.append(('toDate', params['to_date']))  # noqa: E501
            collection_formats['toDate'] = 'multi'  # noqa: E501

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
            '/api/festivals/current/events.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Events',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_event_by_id(self, event_id, **kwargs):  # noqa: E501
        """Find event by ID  # noqa: E501

        Returns a single event  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_event_by_id(event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int event_id: ID of event to return (required)
        :param str accept_language: request specific language
        :return: Event
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_event_by_id_with_http_info(event_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_event_by_id_with_http_info(event_id, **kwargs)  # noqa: E501
            return data

    def get_event_by_id_with_http_info(self, event_id, **kwargs):  # noqa: E501
        """Find event by ID  # noqa: E501

        Returns a single event  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_event_by_id_with_http_info(event_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int event_id: ID of event to return (required)
        :param str accept_language: request specific language
        :return: Event
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['event_id', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_event_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'event_id' is set
        if ('event_id' not in params or
                params['event_id'] is None):
            raise ValueError("Missing the required parameter `event_id` when calling `get_event_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'event_id' in params:
            path_params['eventId'] = params['event_id']  # noqa: E501

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
            '/api/events/{eventId}.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Event',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_events_by_name(self, event_name, **kwargs):  # noqa: E501
        """Find events by name  # noqa: E501

        Returns all events with the given name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_events_by_name(event_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str event_name: Name of events to return (required)
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_events_by_name_with_http_info(event_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_events_by_name_with_http_info(event_name, **kwargs)  # noqa: E501
            return data

    def get_events_by_name_with_http_info(self, event_name, **kwargs):  # noqa: E501
        """Find events by name  # noqa: E501

        Returns all events with the given name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_events_by_name_with_http_info(event_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str event_name: Name of events to return (required)
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['event_name', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_events_by_name" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'event_name' is set
        if ('event_name' not in params or
                params['event_name'] is None):
            raise ValueError("Missing the required parameter `event_name` when calling `get_events_by_name`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'event_name' in params:
            path_params['eventName'] = params['event_name']  # noqa: E501

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
            '/api/events/{eventName}.details.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Events',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_events_by_year(self, year, **kwargs):  # noqa: E501
        """find events by year  # noqa: E501

        returns all published events in the provided year  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_events_by_year(year, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Year of festival for events to return (required)
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int archive: returns all events of archived or not archived festivals<br>Example: /api/events.json?archive=1
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_events_by_year_with_http_info(year, **kwargs)  # noqa: E501
        else:
            (data) = self.get_events_by_year_with_http_info(year, **kwargs)  # noqa: E501
            return data

    def get_events_by_year_with_http_info(self, year, **kwargs):  # noqa: E501
        """find events by year  # noqa: E501

        returns all published events in the provided year  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_events_by_year_with_http_info(year, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Year of festival for events to return (required)
        :param list[str] order: Sets the order of returning events (d - descending)<br>Example: /api/events.json?order=[\"location\"]<br>Possible Values:<br> - date<br> - date-d<br> - event<br> - event-d<br> - artist<br> - artist-d<br> - location<br> - location-d
        :param int entries: Number of entries per page to return (standard = 10)<br>Example: /api/events.json?entries=5
        :param int page: Number of page<br>Example: /api/events.json?page=2
        :param int archive: returns all events of archived or not archived festivals<br>Example: /api/events.json?archive=1
        :param list[int] category: returns events that have a category with the given categoryId<br>Example: /api/events.json?category=[100]
        :param list[int] tag: returns events that have a tag with the given tagId<br>Example: /api/events.json?tag=[100]
        :param list[int] accessible: returns events that have a accessibility with the given accessibilityID<br>Example: /api/events.json?accessible=[100]
        :param list[int] location: returns events that have a location with the given locationID<br>Example: /api/events.json?location=[100]
        :param list[str] time: returns events with event dates in the given timeframe<br>Example: /api/events.json?time=[\"today\"]<br>Possible Values:<br> - today<br> - upcoming<br> - past
        :param list[str] from_date: returns events with event dates from the given date<br>Example: /api/events.json?fromDate=[\"2022-02-14 00:00:00\"]
        :param list[str] to_date: returns events with event dates to the given date<br>Example: /api/events.json?toDate=[\"2022-02-14 00:00:00\"]
        :param str accept_language: request specific language
        :return: Events
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['year', 'order', 'entries', 'page', 'archive', 'category', 'tag', 'accessible', 'location', 'time', 'from_date', 'to_date', 'accept_language']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_events_by_year" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'year' is set
        if ('year' not in params or
                params['year'] is None):
            raise ValueError("Missing the required parameter `year` when calling `get_events_by_year`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'year' in params:
            path_params['year'] = params['year']  # noqa: E501

        query_params = []
        if 'order' in params:
            query_params.append(('order', params['order']))  # noqa: E501
            collection_formats['order'] = 'multi'  # noqa: E501
        if 'entries' in params:
            query_params.append(('entries', params['entries']))  # noqa: E501
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'archive' in params:
            query_params.append(('archive', params['archive']))  # noqa: E501
        if 'category' in params:
            query_params.append(('category', params['category']))  # noqa: E501
            collection_formats['category'] = 'multi'  # noqa: E501
        if 'tag' in params:
            query_params.append(('tag', params['tag']))  # noqa: E501
            collection_formats['tag'] = 'multi'  # noqa: E501
        if 'accessible' in params:
            query_params.append(('accessible', params['accessible']))  # noqa: E501
            collection_formats['accessible'] = 'multi'  # noqa: E501
        if 'location' in params:
            query_params.append(('location', params['location']))  # noqa: E501
            collection_formats['location'] = 'multi'  # noqa: E501
        if 'time' in params:
            query_params.append(('time', params['time']))  # noqa: E501
            collection_formats['time'] = 'multi'  # noqa: E501
        if 'from_date' in params:
            query_params.append(('fromDate', params['from_date']))  # noqa: E501
            collection_formats['fromDate'] = 'multi'  # noqa: E501
        if 'to_date' in params:
            query_params.append(('toDate', params['to_date']))  # noqa: E501
            collection_formats['toDate'] = 'multi'  # noqa: E501

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
            '/api/festivals/{year}/events.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Events',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)