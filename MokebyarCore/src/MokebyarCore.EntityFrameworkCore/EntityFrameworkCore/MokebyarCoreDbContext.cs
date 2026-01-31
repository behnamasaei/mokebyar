using Microsoft.EntityFrameworkCore;
using Volo.Abp.AuditLogging.EntityFrameworkCore;
using Volo.Abp.BackgroundJobs.EntityFrameworkCore;
using Volo.Abp.BlobStoring.Database.EntityFrameworkCore;
using Volo.Abp.Data;
using Volo.Abp.DependencyInjection;
using Volo.Abp.EntityFrameworkCore;
using Volo.Abp.FeatureManagement.EntityFrameworkCore;
using Volo.Abp.Identity;
using Volo.Abp.Identity.EntityFrameworkCore;
using Volo.Abp.PermissionManagement.EntityFrameworkCore;
using Volo.Abp.SettingManagement.EntityFrameworkCore;
using Volo.Abp.OpenIddict.EntityFrameworkCore;
using Volo.Abp.TenantManagement;
using Volo.Abp.TenantManagement.EntityFrameworkCore;
using MokebyarCore.MokebModels;
using Volo.Abp.EntityFrameworkCore.Modeling;

namespace MokebyarCore.EntityFrameworkCore;

[ReplaceDbContext(typeof(IIdentityDbContext))]
[ReplaceDbContext(typeof(ITenantManagementDbContext))]
[ConnectionStringName("Default")]
public class MokebyarCoreDbContext :
    AbpDbContext<MokebyarCoreDbContext>,
    ITenantManagementDbContext,
    IIdentityDbContext
{
    /* Add DbSet properties for your Aggregate Roots / Entities here. */


    #region Entities from the modules

    /* Notice: We only implemented IIdentityProDbContext and ISaasDbContext
     * and replaced them for this DbContext. This allows you to perform JOIN
     * queries for the entities of these modules over the repositories easily. You
     * typically don't need that for other modules. But, if you need, you can
     * implement the DbContext interface of the needed module and use ReplaceDbContext
     * attribute just like IIdentityProDbContext and ISaasDbContext.
     *
     * More info: Replacing a DbContext of a module ensures that the related module
     * uses this DbContext on runtime. Otherwise, it will use its own DbContext class.
     */

    // Identity
    public DbSet<IdentityUser> Users { get; set; }
    public DbSet<IdentityRole> Roles { get; set; }
    public DbSet<IdentityClaimType> ClaimTypes { get; set; }
    public DbSet<OrganizationUnit> OrganizationUnits { get; set; }
    public DbSet<IdentitySecurityLog> SecurityLogs { get; set; }
    public DbSet<IdentityLinkUser> LinkUsers { get; set; }
    public DbSet<IdentityUserDelegation> UserDelegations { get; set; }
    public DbSet<IdentitySession> Sessions { get; set; }

    // Tenant Management
    public DbSet<Tenant> Tenants { get; set; }
    public DbSet<TenantConnectionString> TenantConnectionStrings { get; set; }

    #endregion

    public DbSet<Mokeb> Mokebs { get; set; }
    public DbSet<MokebManager> MokebManagers { get; set; }
    public DbSet<Pilgrim> Pilgrims { get; set; }
    public DbSet<Reservation> Reservations { get; set; }
    public DbSet<Traffic> Traffics { get; set; }

    public MokebyarCoreDbContext(DbContextOptions<MokebyarCoreDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        /* Include modules to your migration db context */

        builder.ConfigurePermissionManagement();
        builder.ConfigureSettingManagement();
        builder.ConfigureBackgroundJobs();
        builder.ConfigureAuditLogging();
        builder.ConfigureFeatureManagement();
        builder.ConfigureIdentity();
        builder.ConfigureOpenIddict();
        builder.ConfigureTenantManagement();
        builder.ConfigureBlobStoring();

        /* Configure your own tables/entities inside here */

        builder.Entity<Mokeb>(b =>
        {
            b.ToTable(MokebyarCoreConsts.DbTablePrefix + "Mokeb", MokebyarCoreConsts.DbSchema);
            b.ConfigureByConvention();
            b.Property(x => x.Name).HasMaxLength(300).IsRequired();
            b.Property(x => x.Address).HasMaxLength(500).IsRequired();
            b.Property(x => x.Location).HasMaxLength(500).IsRequired();
            b.Property(x => x.Phone).HasMaxLength(20).IsRequired();
            b.Property(x => x.Capacity).HasMaxLength(10_000).IsRequired();
            b.Property(x => x.Gender).IsRequired();

            b.HasOne(x => x.MokebManager)
                .WithMany(x => x.Mokebs)
                .HasForeignKey(x => x.MokebManagerId);
            b.HasMany(x => x.Reservations)
                .WithOne(x => x.Mokeb)
                .HasForeignKey(x => x.MokebId);
            b.HasMany(x => x.Traffics)
                .WithOne(x => x.Mokeb)
                .HasForeignKey(x => x.MokebId);
        });

        builder.Entity<MokebManager>(b =>
        {
            b.ToTable(MokebyarCoreConsts.DbTablePrefix + "MokebManager", MokebyarCoreConsts.DbSchema);
            b.ConfigureByConvention();
            b.Property(x => x.Code).HasMaxLength(300).IsRequired();
            b.Property(x => x.ManagerName).HasMaxLength(500).IsRequired();
            b.Property(x => x.ManagerPhone).HasMaxLength(20).IsRequired();
            b.Property(x => x.Address).HasMaxLength(500).IsRequired();
            b.Property(x => x.Location).HasMaxLength(500).IsRequired();

            b.HasMany(x => x.Mokebs)
                .WithOne(x => x.MokebManager)
                .HasForeignKey(x => x.MokebManagerId);
        });

        builder.Entity<Pilgrim>(b =>
        {
            b.ToTable(MokebyarCoreConsts.DbTablePrefix + "Pilgrim", MokebyarCoreConsts.DbSchema);
            b.ConfigureByConvention();
            b.Property(x => x.FirstName).HasMaxLength(200);
            b.Property(x => x.LastName).HasMaxLength(200);
            b.Property(x => x.PassportNumber).HasMaxLength(200);
            b.Property(x => x.Gender);
            b.Property(x => x.Address).HasMaxLength(300);
            b.Property(x => x.Phone).HasMaxLength(20);
            b.Property(x => x.Nationality).HasMaxLength(100);
            b.Property(x => x.State).HasMaxLength(150);
            b.Property(x => x.City).HasMaxLength(150);
            b.HasIndex(x => x.PassportNumber).IsUnique();

            b.HasMany(x => x.Reservations)
                .WithOne(x => x.Pilgrim)
                .HasForeignKey(x => x.PilgrimId);
            b.HasMany(x => x.Traffics)
                .WithOne(x => x.Pilgrim)
                .HasForeignKey(x => x.PilgrimId);
        });

        builder.Entity<Reservation>(b =>
        {
            b.ToTable(MokebyarCoreConsts.DbTablePrefix + "Reservation", MokebyarCoreConsts.DbSchema);
            b.ConfigureByConvention();

            b.HasOne(x => x.Pilgrim)
                .WithMany(x => x.Reservations)
                .HasForeignKey(x => x.PilgrimId);
            b.HasOne(x => x.Mokeb)
                .WithMany(x => x.Reservations)
                .HasForeignKey(x => x.MokebId);
            b.HasMany(x => x.Traffics)
                .WithOne(x => x.Reservation)
                .HasForeignKey(x => x.ReservationId);
        });


        builder.Entity<Traffic>(b =>
        {
            b.ToTable(MokebyarCoreConsts.DbTablePrefix + "Traffic", MokebyarCoreConsts.DbSchema);
            b.ConfigureByConvention();
            b.HasKey(x => new { x.MokebId, x.ReservationId, x.PilgrimId, x.Time });

            b.HasOne(x => x.Pilgrim)
                .WithMany(x => x.Traffics)
                .HasForeignKey(x => x.PilgrimId);
            b.HasOne(x => x.Mokeb)
                .WithMany(x => x.Traffics)
                .HasForeignKey(x => x.MokebId);
            b.HasOne(x => x.Reservation)
                .WithMany(x => x.Traffics)
                .HasForeignKey(x => x.ReservationId)
                .OnDelete(DeleteBehavior.NoAction);
        });
    }
}