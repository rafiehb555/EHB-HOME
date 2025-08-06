import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any

from backend.api_integrations import service_manager, Config


#!/usr/bin/env python3
"""
EHB Home Page - API Integration Tests
Test all external API integrations and services
"""

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))


class IntegrationTester:
    """Test all API integrations"""

    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()

    async def test_aws_services(self) -> Dict[str, Any]:
        """Test AWS services"""
        print("🔍 Testing AWS Services...")

        results = {
            "s3_upload": False,
            "s3_download": False,
            "ses_email": False,
            "cognito_user": False,
        }

        try:
            # Test S3 upload
            test_data = b"Hello EHB World!"
            upload_result = await service_manager.aws.upload_file(
                "test/test-file.txt", test_data, "text/plain"
            )
            results["s3_upload"] = upload_result["success"]

            # Test S3 download
            download_result = await service_manager.aws.get_file("test/test-file.txt")
            results["s3_download"] = download_result["success"]

            # Test SES email (if configured)
            if Config.AWS_ACCESS_KEY_ID:
                email_result = await service_manager.aws.send_email(
                    "test@example.com", "EHB Test Email", "<h1>Hello from EHB!</h1>"
                )
                results["ses_email"] = email_result["success"]

            print(f"✅ AWS Services: {sum(results.values())}/{len(results)} passed")

        except Exception as e:
            print(f"❌ AWS Services failed: {str(e)}")

        return results

    async def test_google_services(self) -> Dict[str, Any]:
        """Test Google Cloud services"""
        print("🔍 Testing Google Cloud Services...")

        results = {
            "storage_upload": False,
            "vision_analysis": False,
            "translate": False,
        }

        try:
            # Test Google Storage upload
            test_data = b"Hello Google Cloud!"
            upload_result = await service_manager.google.upload_to_storage(
                Config.GOOGLE_CLOUD_STORAGE_BUCKET or "test-bucket",
                "test/google-test.txt",
                test_data,
            )
            results["storage_upload"] = upload_result["success"]

            # Test Vision API (if configured)
            if Config.GOOGLE_AI_API_KEY:
                vision_result = await service_manager.google.analyze_image(
                    "https://example.com/test-image.jpg"
                )
                results["vision_analysis"] = vision_result["success"]

            # Test Translate API
            translate_result = await service_manager.google.translate_text(
                "Hello World", "es"
            )
            results["translate"] = translate_result["success"]

            print(
                f"✅ Google Cloud Services: {sum(results.values())}/{len(results)} passed"
            )

        except Exception as e:
            print(f"❌ Google Cloud Services failed: {str(e)}")

        return results

    async def test_ai_services(self) -> Dict[str, Any]:
        """Test AI services"""
        print("🔍 Testing AI Services...")

        results = {
            "openai": False,
            "anthropic": False,
            "google_ai": False,
            "huggingface": False,
        }

        try:
            # Test OpenAI
            if Config.OPENAI_API_KEY:
                openai_result = await service_manager.ai.generate_openai_text(
                    "Say hello to EHB"
                )
                results["openai"] = openai_result["success"]

            # Test Anthropic
            if Config.ANTHROPIC_API_KEY:
                anthropic_result = await service_manager.ai.generate_claude_response(
                    "Say hello to EHB"
                )
                results["anthropic"] = anthropic_result["success"]

            # Test Google AI
            if Config.GOOGLE_AI_API_KEY:
                google_result = await service_manager.ai.generate_gemini_response(
                    "Say hello to EHB"
                )
                results["google_ai"] = google_result["success"]

            # Test Hugging Face
            if Config.HUGGINGFACE_API_KEY:
                hf_result = await service_manager.ai.generate_huggingface_response(
                    "Hello EHB"
                )
                results["huggingface"] = hf_result["success"]

            print(f"✅ AI Services: {sum(results.values())}/{len(results)} passed")

        except Exception as e:
            print(f"❌ AI Services failed: {str(e)}")

        return results

    async def test_payment_services(self) -> Dict[str, Any]:
        """Test payment services"""
        print("🔍 Testing Payment Services...")

        results = {
            "stripe_payment_intent": False,
            "stripe_customer": False,
            "paypal_order": False,
        }

        try:
            # Test Stripe Payment Intent
            if Config.STRIPE_SECRET_KEY:
                stripe_result = (
                    await service_manager.payments.create_stripe_payment_intent(
                        1000, "usd"  # $10.00
                    )
                )
                results["stripe_payment_intent"] = stripe_result["success"]

                # Test Stripe Customer
                customer_result = await service_manager.payments.create_stripe_customer(
                    "test@ehb.com", "Test User"
                )
                results["stripe_customer"] = customer_result["success"]

            # Test PayPal Order
            if Config.PAYPAL_CLIENT_ID:
                paypal_result = await service_manager.payments.create_paypal_order(
                    10.00, "USD"
                )
                results["paypal_order"] = paypal_result["success"]

            print(f"✅ Payment Services: {sum(results.values())}/{len(results)} passed")

        except Exception as e:
            print(f"❌ Payment Services failed: {str(e)}")

        return results

    async def test_communication_services(self) -> Dict[str, Any]:
        """Test communication services"""
        print("🔍 Testing Communication Services...")

        results = {
            "sendgrid_email": False,
            "twilio_sms": False,
            "slack_message": False,
            "telegram_message": False,
        }

        try:
            # Test SendGrid Email
            if Config.SENDGRID_API_KEY:
                email_result = await service_manager.communication.send_email(
                    "test@example.com", "EHB Test Email", "<h1>Hello from EHB!</h1>"
                )
                results["sendgrid_email"] = email_result["success"]

            # Test Twilio SMS
            if Config.TWILIO_ACCOUNT_SID:
                sms_result = await service_manager.communication.send_sms(
                    "+1234567890", "Hello from EHB!"
                )
                results["twilio_sms"] = sms_result["success"]

            # Test Slack Message
            if Config.SLACK_BOT_TOKEN:
                slack_result = await service_manager.communication.send_slack_message(
                    "#general", "Hello from EHB!"
                )
                results["slack_message"] = slack_result["success"]

            # Test Telegram Message
            if Config.TELEGRAM_BOT_TOKEN:
                telegram_result = (
                    await service_manager.communication.send_telegram_message(
                        "123456789", "Hello from EHB!"
                    )
                )
                results["telegram_message"] = telegram_result["success"]

            print(
                f"✅ Communication Services: {sum(results.values())}/{len(results)} passed"
            )

        except Exception as e:
            print(f"❌ Communication Services failed: {str(e)}")

        return results

    async def test_database_services(self) -> Dict[str, Any]:
        """Test database services"""
        print("🔍 Testing Database Services...")

        results = {"redis_set": False, "redis_get": False, "postgres_query": False}

        try:
            # Test Redis operations
            redis_set = await service_manager.database.set_redis_value(
                "test_key", "test_value", 60
            )
            results["redis_set"] = redis_set

            redis_get = await service_manager.database.get_redis_value("test_key")
            results["redis_get"] = redis_get == b"test_value"

            # Test PostgreSQL query
            if Config.DATABASE_URL:
                query_result = await service_manager.database.execute_query(
                    "SELECT 1 as test"
                )
                results["postgres_query"] = len(query_result) > 0

            print(
                f"✅ Database Services: {sum(results.values())}/{len(results)} passed"
            )

        except Exception as e:
            print(f"❌ Database Services failed: {str(e)}")

        return results

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🚀 Starting EHB API Integration Tests...")
        print("=" * 50)

        # Initialize services
        init_success = await service_manager.initialize()
        if not init_success:
            print("❌ Service initialization failed")
            return {}

        # Run all tests
        self.results = {
            "aws_services": await self.test_aws_services(),
            "google_services": await self.test_google_services(),
            "ai_services": await self.test_ai_services(),
            "payment_services": await self.test_payment_services(),
            "communication_services": await self.test_communication_services(),
            "database_services": await self.test_database_services(),
        }

        # Cleanup
        await service_manager.cleanup()

        return self.results

    def generate_report(self) -> str:
        """Generate a comprehensive test report"""
        if not self.results:
            return "No test results available"

        total_tests = 0
        passed_tests = 0
        report_lines = []

        report_lines.append("📊 EHB API Integration Test Report")
        report_lines.append("=" * 50)
        report_lines.append(
            f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append("")

        for service_name, service_results in self.results.items():
            service_passed = sum(service_results.values())
            service_total = len(service_results)
            total_tests += service_total
            passed_tests += service_passed

            status = (
                "✅ PASS"
                if service_passed == service_total
                else "⚠️  PARTIAL" if service_passed > 0 else "❌ FAIL"
            )

            report_lines.append(f"{service_name.replace('_', ' ').title()}: {status}")
            report_lines.append(f"  Passed: {service_passed}/{service_total}")

            for test_name, test_result in service_results.items():
                test_status = "✅" if test_result else "❌"
                report_lines.append(f"    {test_status} {test_name}")
            report_lines.append("")

        # Overall summary
        overall_status = (
            "✅ ALL PASSED"
            if passed_tests == total_tests
            else "⚠️  PARTIAL" if passed_tests > 0 else "❌ ALL FAILED"
        )
        report_lines.append("=" * 50)
        report_lines.append(f"Overall Status: {overall_status}")
        report_lines.append(f"Total Tests: {total_tests}")
        report_lines.append(f"Passed: {passed_tests}")
        report_lines.append(f"Failed: {total_tests - passed_tests}")
        report_lines.append(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        return "\n".join(report_lines)


async def main():
    """Main test function"""
    tester = IntegrationTester()

    try:
        # Run all tests
        await tester.run_all_tests()

        # Generate and print report
        report = tester.generate_report()
        print("\n" + "=" * 50)
        print(report)

        # Save report to file
        with open("integration_test_report.txt", "w") as f:
            f.write(report)

        print(f"\n📄 Report saved to: integration_test_report.txt")

    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
