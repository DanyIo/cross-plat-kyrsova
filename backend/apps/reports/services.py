from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from apps.transactions.models import Transaction
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import FileResponse
import datetime
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import FileResponse
import datetime


class ReportService:
    def __init__(self, user):
        self.user = user

    def get_monthly_yearly_data(self):
        monthly = (
            Transaction.objects.filter(user=self.user)
            .annotate(month=TruncMonth("date"))
            .values("month", "transaction_type")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        yearly = (
            Transaction.objects.filter(user=self.user)
            .annotate(year=TruncYear("date"))
            .values("year", "transaction_type")
            .annotate(total=Sum("amount"))
            .order_by("year")
        )

        return {"monthly": list(monthly), "yearly": list(yearly)}

    def generate_pdf(self):
        try:
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter  # Standard letter size

            # Add Title with Emoji
            p.setFont("Helvetica-Bold", 18)
            p.drawString(
                100, height - 100, f"Financial Report for {self.user.username}"
            )

            # Add Subtitle
            p.setFont("Helvetica", 12)
            p.setFillColor(colors.grey)
            p.drawString(
                100,
                height - 120,
                f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            )

            # Add Spacing
            y_position = height - 160

            # Add Monthly Data Section with formatting
            p.setFont("Helvetica-Bold", 14)
            p.drawString(100, y_position, "Monthly Summary:")
            y_position -= 20

            # Add table header
            p.setFont("Helvetica-Bold", 10)
            p.setFillColor(colors.black)
            p.drawString(100, y_position, "Month")
            p.drawString(250, y_position, "Type")
            p.drawString(400, y_position, "Total")
            y_position -= 20

            p.setFont("Helvetica", 10)
            data = self.get_monthly_yearly_data()

            # Loop through data and add it to the PDF
            for record in data["monthly"]:
                # Format date and transaction type
                formatted_date = record["month"].strftime("%Y-%m")
                transaction_type = record["transaction_type"].capitalize()
                total = f"${record['total']:,.2f}"

                # Draw row data
                p.drawString(100, y_position, formatted_date)
                p.drawString(250, y_position, transaction_type)
                p.drawString(400, y_position, total)
                y_position -= 20

            # Add Spacing Before Footer
            y_position -= 20
            p.setFont("Helvetica-Bold", 12)

            # Add Footer with Emojis
            p.drawString(
                100, y_position, "Thank you for using our Financial Assistant! "
            )
            p.setFont("Helvetica", 10)
            y_position -= 20
            p.drawString(
                100,
                y_position,
                "For more information, visit: www.financialassistant.com",
            )

            # Save PDF
            p.showPage()
            p.save()

            buffer.seek(0)

            return FileResponse(
                buffer, as_attachment=True, filename="financial_report.pdf"
            )

        except Exception as e:
            print(f"Error generating PDF: {e}")  # Log error
            return HttpResponse("Error generating PDF", status=500)
