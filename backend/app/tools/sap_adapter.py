"""
Mock SAP S/4HANA Adapter
Simulates SAP API calls for demo purposes
"""
import os
from datetime import datetime
from typing import Dict, Any
from ..models.schemas import SAPUpdateResponse


class SAPAdapter:
    """Adapter for SAP S/4HANA integration (mock mode for demo)"""

    def __init__(self):
        self.mode = os.getenv("SAP_MODE", "mock")
        self.api_url = os.getenv("SAP_API_URL", "")
        self.api_key = os.getenv("SAP_API_KEY", "")

        # Mock database for demo
        self.mock_customers = {}

    def update_credit_limit(self, customer_id: str, new_limit: float, reason: str) -> SAPUpdateResponse:
        """Update credit limit in SAP"""
        if self.mode == "mock":
            return self._mock_update_credit_limit(customer_id, new_limit, reason)
        else:
            return self._real_update_credit_limit(customer_id, new_limit, reason)

    def update_credit_block(self, customer_id: str, block_flag: bool, reason: str) -> SAPUpdateResponse:
        """Update credit block status in SAP"""
        if self.mode == "mock":
            return self._mock_update_credit_block(customer_id, block_flag, reason)
        else:
            return self._real_update_credit_block(customer_id, block_flag, reason)

    def _mock_update_credit_limit(self, customer_id: str, new_limit: float, reason: str) -> SAPUpdateResponse:
        """Mock implementation"""
        sap_ref = f"SAP-LIM-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Update mock database
        if customer_id not in self.mock_customers:
            self.mock_customers[customer_id] = {}

        self.mock_customers[customer_id]["credit_limit"] = new_limit

        return SAPUpdateResponse(
            success=True,
            sap_reference_id=sap_ref,
            action_taken=f"Credit limit updated to {new_limit:,.2f} INR. Reason: {reason}",
            timestamp=datetime.now()
        )

    def _mock_update_credit_block(self, customer_id: str, block_flag: bool, reason: str) -> SAPUpdateResponse:
        """Mock implementation"""
        sap_ref = f"SAP-BLK-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Update mock database
        if customer_id not in self.mock_customers:
            self.mock_customers[customer_id] = {}

        self.mock_customers[customer_id]["credit_block"] = block_flag

        action = "activated" if block_flag else "released"

        return SAPUpdateResponse(
            success=True,
            sap_reference_id=sap_ref,
            action_taken=f"Credit block {action}. Reason: {reason}",
            timestamp=datetime.now()
        )

    def _real_update_credit_limit(self, customer_id: str, new_limit: float, reason: str) -> SAPUpdateResponse:
        """Real SAP API implementation (placeholder)"""
        # TODO: Implement real SAP OData API calls
        # Example:
        # response = httpx.post(
        #     f"{self.api_url}/A_Customer('{customer_id}')",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={"CreditLimit": new_limit}
        # )
        raise NotImplementedError("Real SAP integration not implemented")

    def _real_update_credit_block(self, customer_id: str, block_flag: bool, reason: str) -> SAPUpdateResponse:
        """Real SAP API implementation (placeholder)"""
        # TODO: Implement real SAP OData API calls
        raise NotImplementedError("Real SAP integration not implemented")


# Singleton instance
sap_adapter = SAPAdapter()
