import pytest

import falcon
import falcon.status_codes as status


@pytest.mark.parametrize('err, title', [
    (falcon.HTTPBadRequest, status.HTTP_400),
    (falcon.HTTPForbidden, status.HTTP_403),
    (falcon.HTTPConflict, status.HTTP_409),
    (falcon.HTTPLengthRequired, status.HTTP_411),
    (falcon.HTTPPreconditionFailed, status.HTTP_412),
    (falcon.HTTPRequestEntityTooLarge, status.HTTP_413),
    (falcon.HTTPUriTooLong, status.HTTP_414),
    (falcon.HTTPUnprocessableEntity, status.HTTP_422),
    (falcon.HTTPLocked, status.HTTP_423),
    (falcon.HTTPFailedDependency, status.HTTP_424),
    (falcon.HTTPPreconditionRequired, status.HTTP_428),
    (falcon.HTTPTooManyRequests, status.HTTP_429),
    (falcon.HTTPRequestHeaderFieldsTooLarge, status.HTTP_431),
    (falcon.HTTPUnavailableForLegalReasons, status.HTTP_451),
    (falcon.HTTPInternalServerError, status.HTTP_500),
    (falcon.HTTPBadGateway, status.HTTP_502),
    (falcon.HTTPServiceUnavailable, status.HTTP_503),
    (falcon.HTTPInsufficientStorage, status.HTTP_507),
    (falcon.HTTPLoopDetected, status.HTTP_508),
    (falcon.HTTPNetworkAuthenticationRequired, status.HTTP_511),
])
def test_with_default_title_and_desc(err, title):
    with pytest.raises(err) as e:
        raise err()

    assert e.value.title == title
    assert e.value.description is None

    if e.value.headers:
        assert 'Retry-After' not in e.value.headers


@pytest.mark.parametrize('err', [
    falcon.HTTPBadRequest,
    falcon.HTTPForbidden,
    falcon.HTTPConflict,
    falcon.HTTPLengthRequired,
    falcon.HTTPPreconditionFailed,
    falcon.HTTPPreconditionRequired,
    falcon.HTTPUriTooLong,
    falcon.HTTPUnprocessableEntity,
    falcon.HTTPLocked,
    falcon.HTTPFailedDependency,
    falcon.HTTPRequestHeaderFieldsTooLarge,
    falcon.HTTPInternalServerError,
    falcon.HTTPUnavailableForLegalReasons,
    falcon.HTTPBadGateway,
    falcon.HTTPInsufficientStorage,
    falcon.HTTPLoopDetected,
    falcon.HTTPNetworkAuthenticationRequired,
])
def test_with_title_and_desc(err):
    title = 'trace'
    desc = 'boom'

    with pytest.raises(err) as e:
        raise err(title=title, description=desc)

    assert e.value.title == title
    assert e.value.description == desc


@pytest.mark.parametrize('err', [
    falcon.HTTPServiceUnavailable,
    falcon.HTTPTooManyRequests,
    falcon.HTTPRequestEntityTooLarge,
])
def test_with_retry_after(err):
    with pytest.raises(err) as e:
        raise err(retry_after='123')

    assert e.value.headers['Retry-After'] == '123'


def test_http_unauthorized_no_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPUnauthorized()
    except falcon.HTTPUnauthorized as e:
        assert status.HTTP_401 == e.title
        assert e.description is None
        assert 'WWW-Authenticate' not in e.headers


def test_http_unauthorized_with_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPUnauthorized(
            title='Test',
            description='Testdescription',
            challenges=['Testch']
        )
    except falcon.HTTPUnauthorized as e:
        assert 'Test' == e.title
        assert 'Testdescription' == e.description
        assert 'Testch' == e.headers['WWW-Authenticate']


def test_http_not_acceptable_no_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPNotAcceptable()
    except falcon.HTTPNotAcceptable as e:
        assert e.description is None


def test_http_not_acceptable_with_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPNotAcceptable(description='Testdescription')
    except falcon.HTTPNotAcceptable as e:
        assert 'Testdescription' == e.description


def test_http_unsupported_media_type_no_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPUnsupportedMediaType()
    except falcon.HTTPUnsupportedMediaType as e:
        assert e.description is None


def test_http_unsupported_media_type_with_title_and_desc_and_challenges():
    try:
        raise falcon.HTTPUnsupportedMediaType(description='boom')
    except falcon.HTTPUnsupportedMediaType as e:
        assert e.description == 'boom'


def test_http_error_repr():
    error = falcon.HTTPBadRequest()
    _repr = '<%s: %s>' % (error.__class__.__name__, error.status)
    assert error.__repr__() == _repr
