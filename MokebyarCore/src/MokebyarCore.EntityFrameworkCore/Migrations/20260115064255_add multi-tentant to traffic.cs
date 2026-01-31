using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MokebyarCore.Migrations
{
    /// <inheritdoc />
    public partial class addmultitentanttotraffic : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<Guid>(
                name: "TenantId",
                table: "AppTraffic",
                type: "uniqueidentifier",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "TenantId",
                table: "AppTraffic");
        }
    }
}
