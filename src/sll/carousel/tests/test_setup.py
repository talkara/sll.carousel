from Products.CMFCore.utils import getToolByName
from sll.carousel.tests.base import IntegrationTestCase


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package_installed(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.carousel'))

    def test_browserlayer(self):
        from sll.carousel.browser.interfaces import ISllCarouselLayer
        from plone.browserlayer import utils
        self.failUnless(ISllCarouselLayer in utils.registered_layers())

    def test_cssregistry_configured__applyPrefix(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertTrue(item.getApplyPrefix())

    def test_cssregistry_configured__authenticated(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertFalse(item.getAuthenticated())

    def test_cssregistry_configured__cacheable(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertTrue(item.getCacheable())

    def test_cssregistry_configured__compression(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertEqual(item.getCompression(), 'safe')

    def test_cssregistry_configured__conditionalcomment(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertFalse(item.getConditionalcomment())

    def test_cssregistry_configured__cookable(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertTrue(item.getCookable())

    def test_cssregistry_configured__enabled(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertTrue(item.getEnabled())

    def test_cssregistry_configured__expression(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertFalse(item.getExpression())

    def test_cssregistry_configured__media(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertEqual(item.getMedia(), 'screen')

    def test_cssregistry_configured__rel(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertEqual(item.getRel(), 'stylesheet')

    def test_cssregistry_configured__rendering(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertEqual(item.getRendering(), 'link')

    def test_cssregistry_configured__title(self):
        css = getToolByName(self.portal, 'portal_css')
        item = css.getResource('++resource++sll.carousel.stylesheets/carousel.css')
        self.assertFalse(item.getTitle())

    def test_metadata__dependency__Products_Carousel(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('Carousel'))

    def test_metadata__dependency__sll_basetheme(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(installer.isProductInstalled('sll.basetheme'))

    def test_metadata__version(self):
        setup = getToolByName(self.portal, 'portal_setup')
        self.assertEqual(
            setup.getVersionForProfile('profile-sll.carousel:default'), u'2')

    def test_propertiestool_navtree_properties__metaTypesNotToList(self):
        properties = getToolByName(self.portal, 'portal_properties')
        navtree_properties = getattr(properties, 'navtree_properties')
        self.assertTrue('Carousel Banner' in navtree_properties.getProperty('metaTypesNotToList'))

    def test_rolemap__Carousel_Add_Carousel_Banner__rolesOfPermission(self):
        permission = "Carousel: Add Carousel Banner"
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(permission) if item['selected'] == 'SELECTED']
        roles.sort()
        self.assertEqual(roles, [
            'Manager',
            'Site Administrator'])

    def test_rolemap__Carousel_Add_Carousel_Banner__acquiredRolesAreUsedBy(self):
        permission = "Carousel: Add Carousel Banner"
        self.assertEqual(self.portal.acquiredRolesAreUsedBy(permission), '')

    def test_viewlets__hidden__plone_portalfooter(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontent"
        skinname = "*"
        self.assertEqual(storage.getHidden(manager, skinname), (u'Products.Carousel.viewlet',))

    def test_viewlets__order__plone_portalfooter(self):
        from zope.component import getUtility
        from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
        storage = getUtility(IViewletSettingsStorage)
        manager = "plone.abovecontent"
        skinname = "*"
        self.assertEqual(storage.getOrder(manager, skinname), (
            'Products.Carousel.viewlet', u'plone.path_bar', u'sll.carousel.viewlet'))

    def test_uninstall__package(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.carousel'])
        self.failIf(installer.isProductInstalled('sll.carousel'))

    def test_uninstall__browserlayer(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.carousel'])
        from sll.carousel.browser.interfaces import ISllCarouselLayer
        from plone.browserlayer import utils
        self.failIf(ISllCarouselLayer in utils.registered_layers())

    def test_uninstall__cssregistry(self):
        installer = getToolByName(self.portal, 'portal_quickinstaller')
        installer.uninstallProducts(['sll.carousel'])
        css = getToolByName(self.portal, 'portal_css')
        self.failIf(
            '++resource++sll.carousel.stylesheets/carousel.css' in css.getResourceIds())
