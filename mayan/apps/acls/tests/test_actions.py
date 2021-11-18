from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.document_states.tests.test_actions import ActionTestCase
from mayan.apps.documents.permissions import permission_document_view

from ..workflow_actions import GrantAccessAction, RevokeAccessAction


class ACLActionTestCase(ActionTestCase):
    def test_grant_access_action(self):
        action = GrantAccessAction(
            form_data={
                'content_type': ContentType.objects.get_for_model(model=self.document).pk,
                'object_id': self.document.pk,
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'entry_log': self.entry_log})

        self.assertEqual(self.document.acls.count(), 1)
        self.assertEqual(
            list(self.document.acls.first().permissions.all()),
            [permission_document_view.stored_permission]
        )
        self.assertEqual(self.document.acls.first().role, self._test_case_role)

    def test_revoke_access_action(self):
        self.grant_access(
            obj=self.document, permission=permission_document_view
        )

        action = RevokeAccessAction(
            form_data={
                'content_type': ContentType.objects.get_for_model(model=self.document).pk,
                'object_id': self.document.pk,
                'roles': [self._test_case_role.pk],
                'permissions': [permission_document_view.pk],
            }
        )
        action.execute(context={'entry_log': self.entry_log})

        self.assertEqual(self.document.acls.count(), 0)
